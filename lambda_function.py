from certbot.main import main
import logging
import shutil

from cpanel import cpanel
from constants import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_cert(domain):
    '''Given a domain, run Certbot to obtain a certificate.
    '''
    logger.info('Obtaining cert for %s', domain)
    args = [
        'certonly',
        '--manual',
        '--domains', domain,
        '--preferred-challenges', 'http',
        '--non-interactive',
        '--manual-public-ip-logging-ok',
        '--agree-tos',
        '--force-renewal',
        '--email', CERT_EMAIL,
        # Override directories to allow running without root
        '--config-dir', '/tmp/certbot/config',
        '--work-dir', '/tmp/certbot/work',
        '--logs-dir', '/tmp/certbot/logs',
        # Set verification hooks
        '--manual-auth-hook', 'python3 auth-hook.py',
        '--manual-cleanup-hook', 'python3 cleanup-hook.py',
    ]
    rc = main(args)
    if rc is not None:
        code = int(rc)
        logger.info('Certbot exit code: %d', code)
        if code != 0:
            raise RuntimeError(f'Certbot failed to generate a cert for {domain}')

def install_cert(domain):
    '''Fetch the server certificate and private key from
    /tmp/certbot/config/live/<domain>, then use the CPanel UAPI to install it. On
    success, delete the certificate information.
    '''
    parameters = {'domain': domain}
    base_dir = f'/tmp/certbot/config/live/{domain}/'
    with open(base_dir + 'cert.pem') as f:
        parameters['cert'] = ''.join(f.readlines()).strip()
    with open(base_dir + 'privkey.pem') as f:
        parameters['key'] = ''.join(f.readlines()).strip()

    logger.info('Installing cert for %s', domain)
    try:
        cpanel('SSL/install_ssl', parameters)
    except RuntimeError as e:
        raise RuntimeError(f'Failed to install cert for {domain}: {e}')

    shutil.rmtree(base_dir)

def lambda_handler(event, context):
    for domain in WEBROOTS:
        get_cert(domain)
        install_cert(domain)

if __name__ == '__main__':
    lambda_handler(None, None)