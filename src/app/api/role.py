from flask import Blueprint
from app import db_helper
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

    # TODO: Add membership list to role

    return json.dumps(role)

