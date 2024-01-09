# localai | This file is a recreation of the `openai` library, with the backend calling ollama models running locally
# for now, it calls models that work on the local machine,
# and soon we will implement a system of workers onto whom requests will be offloaded.

# Update: new openai api natively supports choosing ai-server, thus i will be switching to recreating that
# Additionally, after some planning it seems like both approaches may be equally difficult to implement,
# and so I will try writing the approach #2 straight away.

import requests

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
class WorkerManager:
    def __init__(self, data):
        self.data = data


class LocalAI:
    class Chat:
        class Completions:
            # todo: replace with all parameters that are mentioned in either web_spider.py or model_backend.py
            def create(self, *args, **kwargs):
                # Your logic for handling chat completions
                print("create called")
                print(args)
                print(kwargs)

                request_url = self.parent.base_url + 'api/generate'
                params = dict(
                    model=self.parent.model,
                    prompt='what is the meaning of life?',
                    system='talk like a pirate',
                    stream='false'
                )

                print("request sent to:", request_url)
                resp = requests.get(url=request_url, params=params)
                data = resp.json()
                print("response received, data:")
                print(data)

                # todo: replicate the entire returned object: https://github.com/openai/openai-python/blob/f1c7d714914e3321ca2e72839fe2d132a8646e7f/src/openai/resources/chat/completions.py#L224
                return None

            def __init__(self, parent):
                self.parent = parent

        def __init__(self, parent):
            self.parent = parent

            # Create instances of all nested classes
            self.chat = self.Completions(self)

    def __init__(self, base_url='http://localhost:11434/', decentralize=False):
        self.base_url = base_url  # host url
        self.model = 'llama2-uncensored:7b'  # todo: move model selection to the worker-app

        # Create instances of all nested classes
        self.chat = self.Chat(self)
