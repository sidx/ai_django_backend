from client import post_result, get_result
try:
    from urlparse import urljoin
except ImportError:
    from urllib import urljoin
import json

master_url = "http://localhost:8000/"

def process_tasks(ai_data):
    metadata = ai_data['metadata']
    if metadata['intentName'] == "fetch.task":
        result = fetch_tasks(ai_data['parameters'])
        result_dict = json.loads(result)
    elif metadata['intentName'] == "create.task":
        result = create_tasks(ai_data['parameters'])
    elif metadata['intentName'] == "fetch.task - select.number":
        result = do_action_on_task(ai_data['parameters'])
    else:
        return
    return result

def fetch_tasks(param_data):
    url = urljoin(master_url, 'listjson') + '/'
    print '--------------'
    print (url)
    response = get_result(url, param_data)
    return response.content

def create_tasks(param_data):
    return {'status': "success", 'message': "Task Created"}

def do_action_on_task(param_data):
    if param_data['task_action']:
        url = urljoin(master_url, 'do_action') + '/'
        print '--------------'
        print (url)
        response = get_result(url, param_data)
        return response.content
