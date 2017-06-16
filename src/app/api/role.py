from flask import Blueprint
from app.util import db_get
from app.config import DB_ROLES
import json

role = Blueprint('role', __name__, url_prefix='/api/role')

@role.route('/', methods=['GET'])
def get_roles():
    return json.dumps(db_get(DB_ROLES))


@role.route('/<int:id>', methods=['GET'])
def get_role(id):
    roles = db_get(DB_ROLES)

    for role in roles:
        if role['id'] == id:
            return json.dumps(role)

    # TODO: Add membership list to role

    raise Exception()

