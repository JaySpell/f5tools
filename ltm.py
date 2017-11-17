import json
import sys
sys.path.append('/home/jspell/Documents/dev/f5tools/')
import pprint
from f5_custom import F5

# Colors for output to console
W = '\033[0m'  # white (normal)
R = '\033[31m'  # red
G = '\033[32m'  # green
O = '\033[33m'  # orange
B = '\033[34m'  # blue
P = '\033[35m'  # purple


class LTMUtils(F5):

    def __init__(self, site="TMC", use_cache=False, **kwargs):
        self.name = self
        self.use_cache = use_cache
        self.f5type = 'ltm'
        self.site = site
        super(LTMUtils, self).__init__(self.f5type, site=self.site)
        self.base_uri = 'https://{}/mgmt/tm/ltm/'.format(self.server)
        self._get_active_ltm()

    def get_vip_info(self, vip):
        '''
        Will get the info of a VIP
        Depends:
            get_info_json - returns json of pool members

        :param vip:
            Required - must match name for VIP or will fail

        Returns vip
        '''

        # Set total uri
        host_uri = "https://{}".format(self.server)  # host

        # Determine connection state
        if not self.f5con.active_connection():
            self.f5_connect()

        # Set request uri
        request_uri = (
            "https://{}/mgmt/tm/ltm/virtual/{}/".format(self.server,
                                                        vip))

        # Send REST request and place response
        resp = self.session.get(request_uri, verify=False)
        if resp.status_code != 200:
            print('GET {} returned {}'.format(resp.text, resp.status_code))

        # Return response
        return resp

    def get_all_vip(self):
        '''
        Will get the list of all VIP
        Depends:
            get_info_json - returns json of pool members

        Returns all_vip
        '''

        # Set total uri
        host_uri = "https://{}".format(self.server)  # host

        # Determine connection state
        if not self.f5con.active_connection():
            self.f5_connect()

        # Set request uri
        request_uri = (
            "https://{}/mgmt/tm/ltm/virtual/".format(self.server))

        # Send REST request and place response
        resp = self.session.get(request_uri, verify=False)
        if resp.status_code != 200:
            print('GET {} returned {}'.format(resp.text, resp.status_code))

        # Return response
        return resp

    def get_pool_info(self, pool):
        # Set request uri
        request_uri = (
            "https://{}/mgmt/tm/ltm/pool/{}/".format(self.server,
                                                     pool))
        resp = self._get_info(request_uri)

        # Return response
        return resp

    def get_active_f5(self, site):
        pass

    def get_pool_members(self, pool):
        '''
        Will get pool members
        Depends:
            get_info_json - returns json of pool members
            _get_info - returns

        Returns pool_members
        '''
        resp = None
        pool = pool.replace('/', '~')

        # Get the pool info
        pool_info = self.get_pool_info(pool)
        pool_info = pool_info.json()

        if 'membersReference' in pool_info:
            member_uri = pool_info['membersReference']['link'].split('/pool/')[1]
            member_uri = member_uri.split('?')[0]
            request_uri = (
                "https://{}/mgmt/tm/ltm/pool/{}/".format(self.server,
                                                         member_uri))

            # Set request uri
            resp = self._get_info(request_uri)

        return resp

    def get_node_info(self, node):
        # Set total uri
        host_uri = "https://{}".format(self.server)  # host

        # Determine connection state
        if not self.f5con.active_connection():
            self.f5_connect()

        # Set request uri
        request_uri = (
            "https://{}/mgmt/tm/ltm/node/{}/".format(self.server,
                                                     node))

        # Send REST request and place response
        resp = self.session.get(request_uri, verify=False)
        if resp.status_code != 200:
            print('GET {} returned {}'.format(resp.text, resp.status_code))

        # Return response
        return resp

    def set_irule_vip(self, vip, irule, remove_ir=False, s_irules=False):
        '''
        Will set the irule on a VIP
        Depends:
            get_info_json - returns json of pool members

        :param vip:
            Required - must match name for VIP or will fail

        :param irule:
            Required - must match name for irule or will fail

        :param s_irules:
            Optional - save existing irules defaults false

        Returns none
        '''
        # Set uri for vip irule
        vip_name = self.get_vip_fullname(vip)
        e_uri = 'virtual/{}'.format(vip)
        f_uri = self.base_uri + e_uri
        print(R + f_uri + W)

        # Set the post list
        irules = []

        # If s_irules (save irules) is True
        # output current irules and add to post
        if s_irules:
            current_irules = self.get_vip_irules(vip)
            if current_irules is not None:
                irules = current_irules

        if remove_ir:
            # Remove irule if remove irules set
            irules = [rule for rule in irules if rule not in irule]
        else:
            # Append needed irule
            irules.append(irule)

        # Set post for iRule
        post = {"rules": irules}
        v = json.dumps(post)

        print(G + "POST - {}".format(post) + W)
        print(B + "Values - {}".format(v) + W)
        # Post irule to VS
        try:
            self.f5_connect()
            set_irule = self.session.put(f_uri, data=v, verify=False)
            print(O + "{}".format(set_irule.status_code) + W)
            print(O + "{}".format(set_irule.json()) + W)
        except:
            e = sys.exc_info()[0]
            pp.pprint(e)

    def create_f5_object(self, obj_type, obj_info, log_file):
        '''
        Will create F5 object
        Depends:

        :param obj_type:
            Required - must be valid F5 object type

        :param obj_info:
            Required - should be dict with payload of F5 object

        :param log_file:
            Required - should be opened file that function can output to

        Returns none
        '''
        s_log = open('/home/jspell/Documents/dev/success.log', 'a')

        # If valid begin putting together REST POST
        if obj_type in self.valid_objs:
            f_uri = self.base_uri + obj_type
            v = json.dumps(obj_info)
            try:
                self.f5_connect()
                create = self.session.post(f_uri, data=v, verify=False)
                print(create.status_code)
                if create.status_code is not 200:
                    log_file.write(str(create.status_code) + " " +
                                   str(create.content) + '\n')
                else:
                    s_log.write(str(create.status_code) + " " +
                                str(create.content) + '\n')
                    s_log.close()
            except:
                e = sys.exc_info()[0]
                print(R + "Except - {}".format(e) + W)
        else:
            print(R + "{}".format("Invalid object type...") + W)

    def get_vip_fullname(self, vip):
        '''
        Will get the parition / name of a VIP
        Depends:
            get_info_json - returns json of pool members

        :param vip:
            Required - must match name for VIP or will fail

        Returns vip
        '''

        def search_names(vip, j_vip):
            r_vip = None
            for a_vip in j_vip['items']:
                if a_vip['name'].upper() == vip.upper():
                    r_vip = a_vip['fullPath']
            return r_vip

        if not self.use_cache:
            e_uri = "virtual"
            j_vip = self.get_info_json(e_uri)
            vip_name = search_names(vip, j_vip)
        return vip_name

    def get_vip_irules(self, vip):
        # URI for request
        e_uri = "virtual/{}".format(vip)
        vip_info = self.get_info_json(e_uri)
        irules = []

        try:
            # If there are irules associated with VIP
            if vip_info['rules'] is not None:
                rules_list = vip_info['rules']
                # Remove partition name from irule
                for rule in rules_list:
                    irules.append(rule.split('/')[2])
        except:
            e = sys.exc_info()[0]
            print(e)

        return irules

    def _get_active_ltm(self):
        '''
        Sets active LTM
        Returns none
        '''
        e_uri = '/mgmt/tm/cm/device'
        f_uri = 'https://' + self.server + e_uri

        self.f5_connect()
        active_query = self.session.get(f_uri, verify=False)
        j_active = active_query.json()

        for member in j_active['items']:
            if member['failoverState'] == "active":
                self.server = member['hostname']

    def _get_info(self, request_uri):
        # Set total uri
        host_uri = "https://{}".format(self.server)  # host

        # Determine connection state
        if not self.f5con.active_connection():
            self.f5_connect()

        # Send REST request and place response
        resp = self.session.get(request_uri, verify=False)
        if resp.status_code != 200:
            print('GET {} returned {}'.format(resp.text, resp.status_code))

        return resp
