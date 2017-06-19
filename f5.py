import json
import config
from f5restcon import F5RESTCon


class F5(object):

    def __init__(self, **kwargs):
        self.name = self
        self.username = config.get_username()
        self.password = config.get_password()
        self.server = config.get_server()
        self.f5con = F5RESTCon(self.username, self.password, self.server, 'ltm')
