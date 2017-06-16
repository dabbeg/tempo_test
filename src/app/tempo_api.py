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
