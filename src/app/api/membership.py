from flask import Blueprint, request, jsonify
from app import tempo_api, db_helper, util

membership = Blueprint('membership', __name__, url_prefix='/api/membership')

@membership.route('/', methods=['GET'])
def get_memberships():
    return jsonify(tempo_api.get_memberships())


@membership.route('/<int:team_id>/<int:user_id>', methods=['GET'])
def get_membership(team_id, user_id):
    if not tempo_api.membership_exists(team_id, user_id):
        return util.not_found('Membership with team id {} and user id {} was not found.'.format(team_id, user_id))

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
        return util.not_found('Membership with team id {} and user id {} was not found.'.format(team_id, user_id))

    body = request.get_json()
    role_id = body['role_id']
    if not db_helper.get_role(role_id):
        return util.not_found('Role with id {} was not found.'.format(role_id))

    db_helper.remove_membership(team_id, user_id)

    # only add into the membership table if role is not default
    default_role = db_helper.get_default_role()
    if default_role['id'] != role_id:
        membership = { 'team_id': team_id, 'user_id': user_id, 'role_id': role_id }
        db_helper.add_membership(membership)

    return jsonify(membership)

