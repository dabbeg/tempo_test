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

def get_membership(team_id, user_id):
    memberships = _db_get(DB_MEMBERSHIPS)
    for membership in memberships:
        if membership['team_id'] == team_id and membership['user_id'] == user_id:
            return membership
    return None

def get_memberships(role_id):
    memberships = _db_get(DB_MEMBERSHIPS)
    filtered_memberships = []
    for membership in memberships:
        if membership['role_id'] == role_id:
            filtered_memberships.append({ 'team_id': membership['team_id'], 'user_id': membership['user_id'] })
    return filtered_memberships

def add_membership(membership):
    memberships = _db_get(DB_MEMBERSHIPS)
    memberships.append(membership)
    _db_set(DB_MEMBERSHIPS, memberships)

def remove_membership(team_id, user_id):
    memberships = _db_get(DB_MEMBERSHIPS)
    for idx, membership in enumerate(memberships):
        if membership['team_id'] == team_id and membership['user_id'] == user_id:
            del memberships[idx]
            return True
    return False

def remove_memberships_that_exist(mbs):
    memberships = _db_get(DB_MEMBERSHIPS)

    for membership in memberships:
        for idx, mb in enumerate(mbs):
            if membership['team_id'] == mb['team_id'] and membership['user_id'] == mb['user_id']:
                del mbs[idx]
    return mbs



