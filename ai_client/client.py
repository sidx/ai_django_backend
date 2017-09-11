import requests


def post_result(url, parameters):
    headers = {'Authorization': ''}
    params = {}
    params.update(parameters)
    response = requests.post(url, params={}, headers=headers)
    return response

def get_result(url, parameters):
    headers = {'Authorization': ''}
    params = {}
    params.update(parameters)
    response = requests.get(url, params=params, headers=headers)
    return response