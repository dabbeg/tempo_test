from flask import Blueprint
from app import tempo_api
import json

membership = Blueprint('membership', __name__, url_prefix='/api/membership')

@membership.route('/', methods=['GET'])
def get_memberships():
    return json.dumps(tempo_api.get_memberships())

