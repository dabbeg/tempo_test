import requests

def get_json(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    elif respons.status_code == 404:
        return None
    else:
        raise Exception()
