import json
import config
from f5restcon import F5RESTCon


class F5(object):

    def __init__(self, f5type, **kwargs):
        self.name = self
        self.username = config.get_username()
        self.f5type = f5type
        if f5type == 'gtm':
            self.password = config.get_gtm_password()
            self.server = config.get_gtm_server()
        else:
            self.password = config.get_gtm_password()
            self.server = config.get_ltm_server()

    def f5_connect(self):
        self.f5con = F5RESTCon(self.username, self.password,
                               self.server, self.f5type)
        if not self.f5con.active_connection():
            self.session = self.f5con.connect_session()
