import json

config_file = '/home/jspell/f5_config.json'
#name_file = '/home/jspell/Documents/dev/f5migration/new_name.json'
with open(config_file) as config:
    cfg_params = json.load(config)


def get_username():
    return cfg_params[0]['username']


def get_ltm_password():
    return cfg_params[0]['ltm_password']


def get_ltm_server(site):
    return cfg_params[0]['ltm_server'][site]


def get_gtm_server():
    return cfg_params[0]['gtm_server']


def get_gtm_password():
    return cfg_params[0]['gtm_password']


def get_wideip():
    return cfg_params[1]['all_wide_ip']


def get_f5_ltm_obj():
    return cfg_params[0]['ltm_obj']


def get_f5_new_names():
    '''with open(name_file) as all_names:
        names = json.load(all_names)

    return names'''
    pass
