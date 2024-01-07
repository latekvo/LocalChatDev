# localai | This file is a recreation of the `openai` library, with the backend calling ollama models running locally
# for now, it calls models that work on the local machine, soon we will implement a list of servers which can be called
# in order to offload the task of processing the request to them.
# I envision 2 paths that this approach can take:
#   1. LocalChatDev fully manages which IP should talk with which other IP, then routes the requests accordingly
#   2. Each host signs up as a worker and joins a queue of available workers, any task can be ordered to the first worker in the queue.
# While the 2nd approach may seem more reasonable, and definitely is way more optimal,
# offering near 0% downtime contrary to the 50% downtime the first option requires, it is much harder to implement.
# With the option #2 we have to:
#   * Transfer huge contexts between workers,
#   * Have an entire service dedicated to this worker model,
#   * We may have trouble synchronizing talks between multiple agents at once.
# I believe the best approach would be to get it working with approach #1, then transitioning to approach #2 as soon as possible.

class ChatCompletion:
    # class shouldn't be initialized, call directly
    def __int__(self, messages, model):
        self.messages = messages  # context
        self.model = model  # ollama: 'model'

    def create(self, *args, **kwargs):
        print(args)
        print(kwargs)
