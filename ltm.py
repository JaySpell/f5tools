import json
from f5 import F5


class LTMUtils(F5):

    def __init__(self, site="TMC", use_cache=False, **kwargs):
        self.name = self
        self.use_cache = use_cache
        self.f5type = 'ltm'
        self.site = site
        super(LTMUtils, self).__init__(self.f5type, site=self.site)
        self._get_active_ltm()
        self.base_uri = '/mgmt/tm/ltm/'  # set end params uri

    def get_vip_info(self, vip_name):

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
        vs_name = get_vip_name(vip_name)

        self.f5_connect()

    def get_pool_info(ltm_srv, pool_name):
        pass

    def get_active_f5(self, site):
        pass

    def set_irule_vip(self, vip, irule):
        '''
        Will set the irule on a VIP
        D   epends:
            get_info_json - returns json of pool members

        :param vip:
            Required - must match name for VIP or will fail

        :param irule:
            Required - must match name for irule or will fail

        Returns none
        '''
        # Set uri for vip irule
        e_uri = 'virtual/'
        post = {}

    def get_vip_name(self, vip_name):
        def search_names(vip_name, j_vip):
            for vip in j_vip['items']:
                if vip['name'].upper() == vip_name.upper():
                    r_vip = vip['selfLink'].replace('localhost', self.server)
            return vip['selfLink']

        if not self.use_cache:
            self.f5_connect()
            full_uri = "https://{}{}virtual".format(self.server, self.base_uri)
            all_vip = self.session.get(full_uri, verify=False)
            j_vip = all_vip.json()
        vip = search_names(vip_name, j_vip)

        return vip

    def _get_active_ltm(self):
        e_uri = '/mgmt/tm/cm/device'
        full_uri = "https://" + self.server + e_uri
        print(full_uri)

        self.f5_connect()
        active_query = self.session.get(full_uri, verify=False)
        j_active = active_query.json()

        for member in j_active['items']:
            if member['failoverState'] == "active":
                self.server = member['hostname']
