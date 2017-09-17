import requests


def post_result(url, parameters):
    headers = {'Authorization': ''}
    params = {'csrfmiddlewaretoken': '{{ csrf_token }}'}
    params.update(parameters)
    response = requests.post(url, data=params, headers=headers)
    return response

def get_result(url, parameters):
    headers = {'Authorization': ''}
    params = {}
    params.update(parameters)
    response = requests.get(url, params=params, headers=headers)
    return response