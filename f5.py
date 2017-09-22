import json
import f5_config
from f5restcon import F5RESTCon


class F5(object):

    def __init__(self, f5type, **kwargs):
        self.name = self
        self.username = f5_config.get_username()
        self.f5type = f5type
        self.site = kwargs.get("site", "tmc")

        if f5type == 'gtm':
            self.password = f5_config.get_gtm_password()
            self.server = f5_config.get_gtm_server()
        else:
            self.password = f5_config.get_ltm_password()
            self.server = f5_config.get_ltm_server(self.site)
            self.valid_objs = f5_config.get_f5_ltm_obj()

    def f5_connect(self):
        self.f5con = F5RESTCon(self.username, self.password,
                               self.server, self.f5type)
        if not self.f5con.active_connection():
            self.session = self.f5con.connect_session()

    def get_info_json(self, e_uri):
        '''
        Will get info from F5 REST based on end uri
        Depends:
            f5_connect - inherited from F5 class connects

        :param e_uri:
            Required - this is the end of the uri to send for query

        Returns JSON of info
        '''
        full_uri = self.base_uri + e_uri
        info = None

        self.f5_connect()
        query = self.session.get(full_uri, verify=False)

        if query.status_code == 200:
            r_info = query.json()
        else:
            raise NoInfo("No info for query {}...".format(full_uri))

        return r_info
