# localai | This file is a recreation of the `openai` library, with the backend calling ollama models running locally
# for now, it calls models that work on the local machine,
# and soon we will implement a system of workers onto whom requests will be offloaded.
import datetime
import json
import time

# Update: new openai api natively supports choosing ai-server, thus i will be switching to recreating that
# Additionally, after some planning it seems like both approaches may be equally difficult to implement,
# and so I will try writing the approach #2 straight away.

import requests
from types import SimpleNamespace


# todo: write a worker-app
# todo: add a system automatically choosing the most appropriate model, handle this in the worker-app
# due to how 'client' is initialized in other files, distribution will be handled here via a separate singleton class
# todo: append RUN_LOCALLY logic to every instance of openai and OPENAI_API_KEY inside the CAMEL folder (recursive)


# a basic singleton implementation, communicates with all the worker agents
class WorkerManagerMetaclass:
    _instances = {}

    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = super(WorkerManagerMetaclass, self).__call__(*args, **kwargs)
        return self._instances[self]


# won't be used for now, first we have to get rest of the functionality working.
class WorkerManager(WorkerManagerMetaclass):
    def __init__(self, data):
        self.data = data


class LocalAI:
    class Chat:
        class Completions:
            # todo: replace with all parameters that are mentioned in either web_spider.py or model_backend.py
            def create(self, user, messages, max_tokens, *args, **kwargs):
                # all supplied kwargs: ['messages', 'model', 'temperature', 'top_p', 'n', 'stream', 'stop',
                # 'max_tokens', 'presence_penalty', 'frequency_penalty', 'logit_bias', 'user']

                request_url = self.parent.parent.base_url + 'api/generate'
                # this broken formatting wraps the json inside the key of our html form,
                # this is the only accepted formatting by ollama
                # request_headers = {"Content-Type": "application/x-www-form-urlencoded"}
                request_data = {
                    'model': self.parent.parent.model,
                    'prompt': 'hello',
                    'system': 'talk like a pirate',
                }

                response = requests.post(url=request_url, json=request_data, stream=True)
                response.raise_for_status()

                response_stream = response.iter_lines()
                response_list = []

                # a frequent bug with llama-uncensored2 is to have a soft-locked loop of the '\n' token being returned
                # in order to avoid this we have to switch to a stream mode, parsing every incoming token individually
                repeat_counter = 0
                repeat_token = ''

                # convert response to json:
                for chunk in response_stream:
                    chunk_text = json.loads(chunk)['response']
                    chunk_done = json.loads(chunk)['done']

                    if chunk_text == repeat_token:
                        repeat_counter += 1
                    else:
                        repeat_counter = 0
                        repeat_token = chunk_text

                    # print('partial:', chunk_text)
                    # we break early to avoid breaking the response_text string
                    if chunk_done or repeat_counter > 5:
                        response.close()
                        break
                    else:
                        response_list.append(chunk_text)

                print('done')
                print('entirety:', ''.join(response_list))

                # replicate the entire returned object: https://platform.openai.com/docs/api-reference/chat/object
                # todo: i may need to convert this simple namespace into a ChatCompletion class
                # SimpleNamespace just creates an object in place, it's like having a no-name class
                return_object = SimpleNamespace(
                    id=round(time.time() * 1000),  # fixme: timestamp is not really a proper id, works for now
                    object='chat.completion',
                    created=round(time.time() * 1000),
                    model=self.parent.parent.model,
                    system_fingerprint='system_fingerprint-stud',
                    choices=[
                        SimpleNamespace(
                            # this section requires some testing to be completed
                            index=0,
                            message=SimpleNamespace(
                                role='assistant',
                                content=''.join(response_list)
                            ),
                            logprobs=None,  # fixme: this value might be incorrect if it even matters
                            finish_reason='stop'
                        )
                    ],
                    usage=SimpleNamespace(
                        # this section requires some testing to be completed
                        prompt_tokens=0,
                        completion_tokens=len(response_list),
                        total_tokens=len(response_list)
                    )
                )

                return return_object

            def __init__(self, parent):
                self.parent = parent

        def __init__(self, parent):
            self.parent = parent

            # Create instances of all nested classes
            self.completions = self.Completions(self)

    def __init__(self, base_url=None, decentralize=False):
        # base_url will only ever be used when DECENTRALIZE is set to 0 or not set at all
        if base_url:
            self.base_url = base_url
        else:
            self.base_url = 'http://localhost:11434/'

        self.model = 'llama2-uncensored:7b'  # todo: move model selection to the worker-app

        # Create instances of all nested classes
        self.chat = self.Chat(self)
