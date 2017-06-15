from flask import Blueprint

membership = Blueprint('membership', __name__, url_prefix='/api/membership')

@membership.route('/', methods=['GET'])
def get_memberships():
    return "these are the memberships..."
