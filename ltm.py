import json
from f5 import F5


class LTMUtils(F5):

    def __init__(self, use_cache=False, **kwargs):
        super(LTMUtils, self).__init__()
        self.use_cache = use_cache

    def get_vip_info(self, vip_name):
        if not self.f5con.active_connection():
            self.session = self.f5con.connect_session()
        request_uri = (
            "https://{}/mgmt/tm/ltm/virtual/{}/".format(self.server,
                                                        vip_name))
        resp = self.session.get(request_uri, verify=False)
        if resp.status_code != 200:
            print('GET {} returned {}'.format(resp.text, resp.status_code))

        return resp

    def set_vip_irule(self, vip_name, irule):
        pass

    def get_pool_info(ltm_srv, pool_name):
        pass
