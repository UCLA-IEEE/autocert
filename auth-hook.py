import os

from cpanel import cpanel
try:
    from keys import *
except ImportError:
    # Use environment variables instead
    pass

def auth_hook():
    '''Places the verification file in the CPanel webroot.
    '''
    parameters = {
        'file': os.environ['CERTBOT_TOKEN'],
        'content': os.environ['CERTBOT_VALIDATION'],
        'dir': WEBROOTS[os.environ['CERTBOT_DOMAIN']] + '/.well-known/acme-challenge'
    }
    cpanel('Fileman/save_file_content', parameters=parameters)

if __name__ == '__main__':
    auth_hook()