from app.util import get_json
from app.config import TEMPO_API_URL


def get_teams():
    url = '{}/team'.format(TEMPO_API_URL)
    return get_json(url)

def get_team(id):
    url = '{}/team/{}'.format(TEMPO_API_URL, id)
    return get_json(url)
