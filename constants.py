try:
    from keys import *
except ImportError:
    import json
    import os
    CPANEL_SERVER = os.environ['CPANEL_SERVER']
    CPANEL_USERNAME = os.environ['CPANEL_USERNAME']
    CPANEL_TOKEN = os.environ['CPANEL_TOKEN']
    WEBROOTS = json.loads(os.environ['WEBROOTS'])