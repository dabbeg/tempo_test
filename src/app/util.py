import requests

def rest_get(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    elif respons.status_code == 404:
        return None
    else:
        raise Exception()

def not_found(msg):
    return msg, 404
