from client import post_result, get_result
try:
    from urlparse import urljoin
except ImportError:
    from urllib import urljoin
import json

master_url = "http://localhost:8000/"

def process_tasks(ai_data):
    metadata = ai_data['result']['metadata']
    if ai_data['result']['action'] == "fetchtask":
        result = fetch_tasks(ai_data)
        print type(result)
        result_dict = json.loads(result)
    elif ai_data['result']['action'] == "create.task":
        result = create_tasks(ai_data['result']['parameters'])
    elif ai_data['result']['action'] == "fetchtask-selectnumber":
        result = do_action_on_task(ai_data['result']['parameters'])
    else:
        return
    return result

def fetch_tasks(param_data):
    url = urljoin(master_url, 'webhook') + '/'
    print '--------------'
    print (param_data)
    response = post_result(url, param_data)
    return response.content

def create_tasks(param_data):
    url = urljoin(master_url, 'addtodojson') + '/'
    response = post_result(url, param_data)
    return {'status': "success", 'message': "Task Created"}

def do_action_on_task(param_data):
    if param_data['task_action']:
        url = urljoin(master_url, 'do_action') + '/'
        print '--------------'
        print (url)
        response = get_result(url, param_data)
        return response.content
