from app.util import get_json
from app.config import TEMPO_API_URL


def get_users():
    url = '{}/user'.format(TEMPO_API_URL)
    return get_json(url)

def get_user(id):
    url = '{}/user/{}'.format(TEMPO_API_URL, id)
    return get_json(url)
