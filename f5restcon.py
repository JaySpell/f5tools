import requests
import time


class F5RESTCon(object):

    def __init__(self, username, password, server, f5type):
        self.name = self
        self.server = server
        self.username = username
        self.password = password
        self.conection_state = False
        self.lastauthtimestamp = 0
        self.lastactiontimestamp = 0
        self.idletimeout = 500
        self.abstimeout = 1200
        self.sessioncookie = ''
        self.f5type = f5type

    def connect_session(self):
        if not self.active_connection():
            if self.f5type[0].upper() == 'G':
                f5_type = "gtm"
            else:
                f5_type = "ltm"
            print(f5_type)
            self.s = requests.Session()
            self.s.auth = (self.username, self.password)
            r = self.s.get('https://' + self.server +
                           '/mgmt/tm/' + f5_type + '/', verify=False)
        return self.s

    def active_connection(self):
        now = time.time()
        cond1 = now > (self.lastactiontimestamp + self.idletimeout)
        cond2 = now > (self.lastactiontimestamp + self.abstimeout)
        if (cond1 or cond2):
            self.connection_state = False
        else:
            self.connection_state = True
        return self.connection_state

    def reset_auth_vals(self):
        self.lastauthtimestamp = 0
        self.lastactiontimestamp = 0
        self.idletimeout = 0
        self.abstimeout = 0
        self.sessioncookie = ''
