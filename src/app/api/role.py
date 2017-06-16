from flask import Blueprint
from app import tempo_api, db_helper
import json

role = Blueprint('role', __name__, url_prefix='/api/role')

@role.route('/', methods=['GET'])
def get_roles():
    return json.dumps(db_helper.get_roles())


@role.route('/<int:role_id>', methods=['GET'])
def get_role(role_id):
    role = db_helper.get_role(role_id)
    if not role:
        raise Exception()

    memberships = []
    default_role = db_helper.get_default_role()
    if role_id == default_role['id']:
        memberships = tempo_api.get_memberships()
        memberships = db_helper.remove_memberships_that_exist(memberships)
    else:
        memberships = db_helper.get_memberships(role_id)

    role['memberships'] = memberships

    return json.dumps(role)

