import requests
import json
from app import redis
from app.config import DB_ROLES, DB_MEMBERSHIPS

def rest_get(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    elif respons.status_code == 404:
        return None
    else:
        raise Exception()

def init_db():
    _init_roles()
    _init_memberships()

def _init_roles():
    roles = []
    roles.append({ 'id': 1, 'name': 'Developer', 'default': True })
    roles.append({ 'id': 2, 'name': 'Product Owner', 'default': False })
    roles.append({ 'id': 3, 'name': 'Tester', 'default': False })
    db_set(DB_ROLES, roles)

def _init_memberships():
    memberships = []
    db_set(DB_MEMBERSHIPS, memberships)

def db_get(key):
    return json.loads(redis.get(key).decode('utf-8'))

def db_set(key, value):
    redis.set(key, json.dumps(value))
