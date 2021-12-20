import logging
import os

from cpanel import cpanel_delete_file
from constants import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def cleanup_hook():
    '''Deletes verification file from CPanel webroot.

    NOTE: Uses deprecated API via cpanel_delete_file(). Will eventually fail.
    '''
    filepath = WEBROOTS[os.environ['CERTBOT_DOMAIN']] + '/.well-known/acme-challenge' + os.environ['CERTBOT_TOKEN']
    try:
        cpanel_delete_file(filepath)
    except RuntimeError:
        # Since deleting the verification file is not mandatory, simply log a
        # message on failure and continue execution
        logger.info('Failed to delete verification file. CPanel API2 may be no longer be supported.')

if __name__ == '__main__':
    cleanup_hook()