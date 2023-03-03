import requests


def get(object_name, auth=None, parameters=None):
    url = f'http://127.0.0.1:8000/api/{object_name}/'
    try:
        response = requests.get(url, auth=auth, params=parameters, timeout=3)
    except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError) as error:
        return error
    data = response.json()
    return data


def post(object_name, auth=None, data=None):
    url = f'http://127.0.0.1:8000/api/{object_name}/'
    try:
        response = requests.post(url, auth=auth, data=data, timeout=3)
    except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError) as error:
        return error
    return response.json()


def put(object_name, object_id, auth=None, data=None):
    url = f'http://127.0.0.1:8000/api/{object_name}/{object_id}/'
    try:
        response = requests.put(url, auth=auth, json=data, verify=False, timeout=3)
    except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError) as error:
        return error
    return response.json()


def delete(object_name, object_id, auth=None):
    url = f'http://127.0.0.1:8000/api/{object_name}/{object_id}/'
    try:
        response = requests.delete(url, auth=auth, verify=False, timeout=3)
    except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError) as error:
        return error
    return response.ok
