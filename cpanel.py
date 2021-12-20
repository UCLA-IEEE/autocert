import json
import logging
import requests

from constants import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def cpanel(target, parameters=None):
    '''Make a call to the CPanel UAPI at the given target (module/function) with
    parameters and values specified in the parameters dict.
    '''
    target = target.strip('/')
    if not target or '/' not in target:
        raise ValueError('Target must be a non-empty string of the form `module/function`')

    url = f'https://{CPANEL_SERVER}/execute/{target}'
    headers = {'Authorization' : f'cpanel {CPANEL_USERNAME}:{CPANEL_TOKEN}'}
    logger.info('GET %s', target)
    res = requests.get(url, params=parameters, headers=headers)
    logger.info('%s', json.dumps(res.json(), indent=2))
    print(json.dumps(res.json(), indent=2))
    if res.status_code != requests.codes.ok:
        raise RuntimeError(f'Request to {url} returned status code {res.status_code}')

def cpanel_delete_file(filepath):
    '''Deletes the file at filepath from the CPanel server.

    NOTE: Uses deprecated CPanel API2 because no delete file function exists in
    CPanel UAPI. Ideally, this would be replaced with a standard cpanel() call
    once UAPI supports deleting files.
    '''
    url = f'https://{CPANEL_SERVER}/json-api/cpanel'
    headers = {'Authorization' : f'cpanel {CPANEL_USERNAME}:{CPANEL_TOKEN}'}
    parameters = {
        'cpanel_jsonapi_user': CPANEL_USERNAME,
        'cpanel_jsonapi_apiversion': 2,
        'cpanel_jsonapi_module': 'Fileman',
        'cpanel_jsonapi_func': 'fileop',
        'op': 'trash',
        'sourcefiles': filepath
    }
    logger.info('GET Fileman/fileop')
    res = requests.get(url, params=parameters, headers=headers)
    logger.info('%s', json.dumps(res.json(), indent=2))
    print(json.dumps(res.json(), indent=2))
    if res.status_code != requests.codes.ok:
        raise RuntimeError(f'Request to {url} returned status code {res.status_code}')