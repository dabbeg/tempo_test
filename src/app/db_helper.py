from app import redis
from app.config import DB_MEMBERSHIPS, DB_ROLES
import json

def init_db():
    _init_roles()
    _init_memberships()

def _init_roles():
    roles = []
    roles.append({ 'id': 1, 'name': 'Developer', 'default': True })
    roles.append({ 'id': 2, 'name': 'Product Owner', 'default': False })
    roles.append({ 'id': 3, 'name': 'Tester', 'default': False })
    _db_set(DB_ROLES, roles)

def _init_memberships():
    memberships = []
    _db_set(DB_MEMBERSHIPS, memberships)


def _db_get(key):
    return json.loads(redis.get(key).decode('utf-8'))

def _db_set(key, value):
    redis.set(key, json.dumps(value))

def get_roles():
    return _db_get(DB_ROLES)

def get_role(role_id):
    roles = _db_get(DB_ROLES)
    for role in roles:
        if role['id'] == role_id:
            return role
    return None

def get_default_role():
    roles = _db_get(DB_ROLES)
    for role in roles:
        if role['default']:
            return role
    return None

def role_exists(role_id):
    roles = _db_get(DB_ROLES)
    for role in roles:
        if role['id'] == role_id:
            return True
    return False

def get_membership(team_id, user_id):
    memberships = _db_get(DB_MEMBERSHIPS)
    for membership in memberships:
        if membership['team_id'] == team_id and membership['user_id'] == user_id:
            return membership
    return None

def remove_membership(team_id, user_id):
    memberships = _db_get(DB_MEMBERSHIPS)
    for idx, membership in enumerate(memberships):
        if membership['team_id'] == team_id and membership['user_id'] == user_id:
            del memberships[idx]
            return True
    return False

def add_membership(membership):
    memberships = _db_get(DB_MEMBERSHIPS)
    memberships.append(membership)
    _db_set(DB_MEMBERSHIPS, memberships)
