import sys
from adal import AdalError, AuthenticationContext
from pathlib import Path
import json
import requests
from datetime import datetime

import functools

AUTHORITY_URL = 'https://login.microsoftonline.com'
CUR_DIR = Path(__file__).resolve().parent


def _get_token_file_path():
    return Path.home() / '.pods' / 'accessToken.json'


def _read_cached_token():
    path = _get_token_file_path()
    if not path.exists():
        return None
    token = json.loads(path.read_text(encoding='utf-8'))
    return token


def _write_cached_token(token):
    path = _get_token_file_path()
    path.parent.mkdir(exist_ok=True)
    path.touch(mode=0o600, exist_ok=True)
    path.write_text(json.dumps(token, indent=2), encoding='utf-8')


def _get_valide_token_from_cache():
    token = _read_cached_token()
    if token is None:
        return None

    expire_time = datetime.strptime(token['expiresOn'], '%Y-%m-%d %H:%M:%S.%f')
    if expire_time > datetime.now():
        return token['accessToken']

    context = AuthenticationContext(token['_authority'])
    try:
        new_token = context.acquire_token_with_refresh_token(
            token['refreshToken'],
            token['_clientId'],
            token['resource'],
        )
        token = {**token, **new_token}
        _write_cached_token(token)
        return token['accessToken']
    except AdalError:
        print('Get token by refresh token failed.', file=sys.stderr)
        return None


def acquire_token_by_device_code(resource, client_id, tenant_id):
    access_token = _get_valide_token_from_cache()
    if access_token is not None:
        return access_token

    context = AuthenticationContext(f'{AUTHORITY_URL}/{tenant_id}')
    code = context.acquire_user_code(resource, client_id)
    print(code['message'], file=sys.stderr)
    token = context.acquire_token_with_device_code(resource, code, client_id)
    _write_cached_token(token)
    return token['accessToken']


BASE_URL = 'https://vdi-mlops.eastus.cloudapp.azure.com/api/'

resource = 'api://7cc85b49-e3d0-4033-804f-6bc27714828c'
client_id = '4681bd17-032d-4c9f-9408-8998387ecc31'
tenant_id = '72f988bf-86f1-41af-91ab-2d7cd011db47'


def forge_header():
    token = acquire_token_by_device_code(resource, client_id, tenant_id)
    return {'Authorization': f'Bearer {token}'}


def read_cache(key):
    cache_file = CUR_DIR / '.cache' / f'{key}.json'
    if cache_file.exists():
        return json.loads(cache_file.read_text())
    else:
        return None


def write_cache(key, content):
    cache_file = CUR_DIR / '.cache' / f'{key}.json'
    if not cache_file.parent.exists():
        cache_file.parent.mkdir(parents=True)
    cache_file.write_text(json.dumps(content))


@functools.lru_cache()
def make_cached_request(url):
    cache = read_cache(url)
    if cache:
        return cache
    else:
        res = requests.get(f'{BASE_URL}{url}', headers=forge_header())
        if res.status_code == 200:
            res_json = res.json()
            write_cache(url, res_json)
            return res_json
        else:
            raise Exception(res.text)


def get_details_of_record_id(record_id):
    url = f'eval/ocr/records/{record_id}'
    return make_cached_request(url)


def get_eval_file(rel_path):
    url = f'{BASE_URL}eval/blobs/{rel_path}'
    return make_cached_request(url)


def list_eval_dir(storage_root):
    url = f'{BASE_URL}eval/trees/{storage_root}'
    return make_cached_request(url)
