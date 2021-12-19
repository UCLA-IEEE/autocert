import os
import logging
import requests
from requests.api import head

try:
    from keys import *
except ImportError:
    # Use environment variables instead
    pass

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
    logger.info('GET %s', url)
    print(url)
    res = requests.get(url, params=parameters, headers=headers)
    logger.info('%s', res.text)
    if res.status_code != requests.codes.ok:
        raise RuntimeError(f'Request to {url} returned status code {res.status_code}')

def lambda_handler(event, context):
    pass