import requests
import json
from app import redis
from app.config import DB_ROLES

def get_json(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    elif respons.status_code == 404:
        return None
    else:
        raise Exception()

def init_db():
    _init_roles()

def _init_roles():
    roles = []
    roles.append({ 'id': 1, 'name': 'Developer', 'default': True })
    roles.append({ 'id': 2, 'name': 'Product Owner', 'default': False })
    roles.append({ 'id': 3, 'name': 'Tester', 'default': False })
    db_set(DB_ROLES, roles)

def db_get(key):
    return json.loads(redis.get(key).decode('utf-8'))

def db_set(key, value):
    redis.set(key, json.dumps(value))
