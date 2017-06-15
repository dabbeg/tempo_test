from flask import Blueprint

role = Blueprint('role', __name__, url_prefix='/api/role')

@role.route('/', methods=['GET'])
def get_roles():
    return "these are the roles..."
