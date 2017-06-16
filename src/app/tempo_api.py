from app.util import rest_get
from app.config import TEMPO_API_URL

def get_users():
    url = '{}/user'.format(TEMPO_API_URL)
    return rest_get(url)

def get_user(id):
    url = '{}/user/{}'.format(TEMPO_API_URL, id)
    return rest_get(url)

def get_teams():
    url = '{}/team'.format(TEMPO_API_URL)
    return rest_get(url)

def get_team(id):
    url = '{}/team/{}'.format(TEMPO_API_URL, id)
    return rest_get(url)

def get_memberships():
    memberships = []
    teams = get_teams()

    for team in teams:
        team_expand = get_team(team['id'])

        for user_id in team_expand['members']:
            memberships.append({ 'team_id': team['id'], 'user_id': user_id })

    return memberships
