# Autocert

Autocert is a workaround to allow secure installation of Let's Encrypt TLS
certificates to IEEE's shared Namecheap server without needing root access on
the server.

## Running Locally

Although originally intended to be run as an AWS Lambda, Autocert can be run as
a cronjob on a Raspberry Pi or simply locally on any Linux machine with root
access.

To run locally, you will need a file `keys.py` with the following content:
```python
CPANEL_SERVER = '<server name and port>'
CPANEL_USERNAME = '<username>'
CPANEL_TOKEN = '<api token>'

CERT_EMAIL = 'webmaster@ieeebruins.com' # To be associated with cert
WEBROOTS = {
    '<domain name>': f'/home/{CPANEL_USERNAME}/path/to/webroot',
    # Add a new entry for each domain that needs a cert
}
```

You will also need the `certbot` package, which you can install with:
```bash
pip install certbot
```

Then run
```bash
python lambda_function.py
```

This will generate new certificates for new domains and renew old certificates
on previously secured domains, installing them on the server. Since Let's
Encrypt certificates are only valid for 90 days, Autocert should ideally be run
every two months.