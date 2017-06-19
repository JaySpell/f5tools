import json

config_file = '/home/jspell/f5_config.json'
with open(config_file) as config:
    cfg_params = json.load(config)


def get_username():
    return cfg_params[0]['username']


def get_password():
    return cfg_params[0]['password']


def get_server():
    return cfg_params[0]['server']
