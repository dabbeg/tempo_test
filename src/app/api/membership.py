from flask import Blueprint, request, jsonify
from app import tempo_api, db_helper

membership = Blueprint('membership', __name__, url_prefix='/api/membership')

@membership.route('/', methods=['GET'])
def get_memberships():
    return jsonify(tempo_api.get_memberships())


@membership.route('/<int:team_id>/<int:user_id>', methods=['GET'])
def get_membership(team_id, user_id):
    if not tempo_api.membership_exists(team_id, user_id):
        raise Exception()

    role_id = 0
    membership = db_helper.get_membership(team_id, user_id)
    if membership:
        role_id = membership['role_id']
    else:
        role = db_helper.get_default_role()
        role_id = role['id']

    return jsonify({ 'team_id': team_id, 'user_id': user_id, 'role_id': role_id })


@membership.route('/<int:team_id>/<int:user_id>', methods=['PUT'])
def update_membership(team_id, user_id):
    if not tempo_api.membership_exists(team_id, user_id):
        raise Exception()

    body = request.get_json()
    role_id = body['role_id']
    if not db_helper.role_exists(role_id):
        raise Exception()

    db_helper.remove_membership(team_id, user_id)

    membership = { 'team_id': team_id, 'user_id': user_id, 'role_id': role_id }
    db_helper.add_membership(membership)

    return jsonify(membership)

