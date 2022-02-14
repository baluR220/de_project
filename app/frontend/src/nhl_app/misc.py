from requests import get
from .common import API_HOST, API_PORT


def call_update_db():
    url = f'http://{API_HOST}:{API_PORT}/'
    try:
        res = get(url)
        res = {'status': 'ok', 'content': res}
    except Exception:
        res = {'status': 'error', 'content': 'Backend is unreachable'}
    return res
