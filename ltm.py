import json
from f5 import F5


class LTMUtils(F5):

    def __init__(self, site, use_cache=False, **kwargs):
        self.name = self
        self.use_cache = use_cache
        self.server = server
        self.f5type = 'ltm'
        self.base_cmd = '/mgmt/tm/ltm/'  # set end params uri
        super(LTMUtils, self).__init__(self.server, self.f5type)

    def get_vip_info(self, vip_name):
        # Get active F5
        server = get_active_f5()
        # Set total uri
        host_uri = "https://{}".format(self.server)  # host

        # Determine connection state
        if not self.f5con.active_connection():
            self.f5_connect()

        # Set request uri
        request_uri = (
            "https://{}/mgmt/tm/ltm/virtual/{}/".format(self.server,
                                                        vip_name))

        # Send REST request and place response
        resp = self.session.get(request_uri, verify=False)
        if resp.status_code != 200:
            print('GET {} returned {}'.format(resp.text, resp.status_code))

        # Return response
        return resp

    def set_vip_irule(self, vip_name, irule):
        pass

    def get_pool_info(ltm_srv, pool_name):
        pass

    def get_active_f5(self, site):
        pass

    def set_irule_vip(self, vip, irule):
        pass
