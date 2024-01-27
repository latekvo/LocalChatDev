#  AI agent worker is a service listening to tasks put out by the central management server
#  work cycle: pull -> start -> push
import openai
import requests

# this sounds like a catastrophe to work with,
# but right now with how much files i would have to duplicate with the current approach,
# i'm considering using the original repo in it's entirety for both the splitting, processing and combining processes.
# the prompts will have to be modified, and switched on appropriately, but the rest of the code stays the same,
# with both the workers using ChatDev to complete their tasks, and the central server using it to split tasks.
# problems with combining can be solved by combining only 2 tasks at the same time, larger models will be used for this.
# Well, to come back to the other approach, since we are operating on such small tasks, probably only 1 file as well,
# i don't see a point in having all of those other tools available, perhaps git could be useful but that's about it,
# it should suffice to only use a tiny langchain with the 2 aforementioned prompts included, and none of the additional
# bulkiness included.

# tasks will be divided into simple and complex queries, with the former ones being simple completion requests,
# while the complex ones being the routines i described earlier. This will enable the central server to only
# focus on bridging our workers instead of contributing computational power as well.

# todo: if file expands, create a separate Connection file & class
local_api_url = "http://127.0.0.1:5000/v1"
openai.api_version = "2023-05-15"
client = openai.OpenAI(
    organization='LOCAL_WORKER',
    api_key='sk-111111111111111111111111111111111111111111111111',
    base_url=local_api_url
)

def make_simple_request(messages):
    local_url = 'http://127.0.0.1:5000/v1/chat/completions'

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "mode": "chat",
        "messages": messages
        # "character": "Assistant",
    }

    response = requests.post(local_url, headers=headers, json=data, verify=False)
    assistant_message = response.json()['choices'][0]['message']['content']

    return assistant_message


def routine_simple():
    pass


def routine_complex():
    pass


def pull_task():
    # tasks are submodules of the app, we will have to launch the (programmer <-> code reviewer) routine here
    pass


def start_task():
    # parses fetched task(s), launches routines accordingly
    pass


def push_task():
    # returns completed tasks back to the manager
    pass


def get_manager_status(url='http://127.0.0.1', port=''):
    # checks connectivity, informs of any errors, sets global ip variable
    url.removesuffix('/')

    if port != '':
        request_url = url + ':' + port
    else:
        request_url = url

    request_url += '/worker_api/status'

    # this api is intended for status dashboard, we're only checking the readiness indicator
    # todo: status API: {
    #   project_name: string
    #   ready: bool,
    #   tasks: integer,
    #   tasks_completed: integer,
    #   uptime: integer,
    # }
    try:
        result = requests.post(url=request_url)
    except requests.ConnectionError:
        print('Error: could not connect to manager server.')
        result = None
    finally:
        return requests.post(url=request_url)


def get_local_status():
    # 1: check if local API is up and running
    return client.models.list()


def start_worker():
    # Connect to the server, check local readiness, run the task loop

    local_status = get_local_status()
    print(local_status)

    manager_status = get_manager_status()
    print(manager_status)

    pass


# ENTRY POINT:
start_worker()
