# localai | This file is a recreation of the `openai` library, with the backend calling ollama models running locally
# for now, it calls models that work on the local machine,
# and soon we will implement a system of workers onto whom requests will be offloaded.

# Update: new openai api natively supports choosing ai-server, thus i will be switching to recreating that
# Additionally, after some planning it seems like both approaches may be equally difficult to implement,
# and so I will try writing the approach #2 straight away.

import requests

# todo: write a worker-app
# todo: add a system automatically choosing the most appropriate model, handle this in the worker-app

class LocalAI:
    class Chat:
        def __init__(self, parent):
            self.parent = parent

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

            return None

    def __init__(self, base_url='http://localhost:11434/'):
        self.base_url = base_url  # host url
        self.model = 'llama2-uncensored:7b', # todo: move model selection to the worker-app

        # Create instances of all nested classes
        self.chat = self.Chat(self)
