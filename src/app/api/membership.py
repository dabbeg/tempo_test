from flask import Blueprint
from app import tempo_api
from app.config import DB_MEMBERSHIPS, DB_ROLES
from app.util import db_get
import json

membership = Blueprint('membership', __name__, url_prefix='/api/membership')

@membership.route('/', methods=['GET'])
def get_memberships():
    return json.dumps(tempo_api.get_memberships())

@membership.route('/<int:team_id>/<int:user_id>', methods=['GET'])
def get_membership(team_id, user_id):
    if not tempo_api.membership_exists(team_id, user_id):
        raise Exception()

    memberships = db_get(DB_MEMBERSHIPS)
    role_id = 0

    # Check if role for membership is in db
    for membership in memberships:
        if membership['team_id'] == team_id and membership['user_id'] == user_id:
            role_id = membership['role_id']

    # If role was not in db, get default role
    if role_id == 0:
        roles = db_get(DB_ROLES)
        for role in roles:
            if role['default']:
                role_id = role['id']

    if role_id == 0:
        raise Exception()

    return json.dumps({ 'team_id': team_id, 'user_id': user_id, 'role_id': role_id })
