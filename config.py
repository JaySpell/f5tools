import json

config_file = '/home/jspell/f5_config.json'
with open(config_file) as config:
    cfg_params = json.load(config)


def get_username():
    return cfg_params[0]['username']


def get_ltm_password():
    return cfg_params[0]['ltm_password']


def get_ltm_server():
    return cfg_params[0]['ltm_server']


def get_gtm_server():
    return cfg_params[0]['gtm_server']


def get_gtm_password():
    return cfg_params[0]['gtm_password']
