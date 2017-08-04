import json
import sys
sys.path.append('/home/jspell/Documents/dev/f5tools/')
from f5 import F5


class GTMUtils(F5):

    def __init__(self, use_cache=False, **kwargs):
        self.name = self
        self.use_cache = use_cache
        self.f5type = 'gtm'
        super(GTMUtils, self).__init__(self.f5type)
        self.base_uri = 'https://{}/mgmt/tm/gtm/'.format(self.server)

    def switch_primary_gtm_pool(self, pool):

        # Get pool info
        pool_info = self.get_primary_pool_member(pool)

        # If pool info includes members switch 0 & 1 (reverse order)
        if pool_info is not None:

            # Reverse member 1 & member 2
            pool_post = {
                pool_info['s_link']: {"order": 0},
                pool_info['p_link']: {"order": 1}
            }

            # Sent command to reverse
            for k, v in pool_post.items():
                v = json.dumps(v)
                rev_req = self.session.put(k, data=v, verify=False)
                print(k, v)
                print(rev_req.status_code)
                print(rev_req.json())

    def get_gtm_pool(self):
        pass

    def get_primary_pool_member(self, pool):
        '''
        Will return the active site for a pool based on global availability
        '''

        # Set query URI
        e_uri = 'pool/~Common~{}/members'.format(pool)
        full_uri = self.base_uri + e_uri
        site = "MC"

        # Connect to F5 GTM and send query
        pool_info = None
        self.f5_connect()
        pool_query = self.session.get(full_uri, verify=False)

        # If 200 code from response - else return None
        if pool_query.status_code == 200:

            # Output response to JSON
            j_pool = pool_query.json()
            pool_info = {}

            # Search for members - replace localhost
            for member in j_pool['items']:
                if member['order'] == 0:
                    pool_info['p_link'] = member['selfLink'].replace(
                        'localhost',
                        self.server
                    )
                else:
                    pool_info['s_link'] = member['selfLink'].replace(
                        'localhost',
                        self.server
                    )

            # Determine primary site
            if "TMC" in pool_info['p_link']:
                pool_info['site'] = "TMC"
            else:
                pool_info['site'] = "MC"

        return pool_info

    def fallbackip_used(self, pool):
        '''
        Will return a boolean for whether fallbackip used as load balancing
        method for pool.
        Depends:
            get_info_json - returns json of pool members

        :param pool:
            Required - must match name for GTM pool or will fail

        Returns boolean
        '''
        e_uri = 'pool/~Common~{}'.format(pool)
        fip = False

        try:
            pool_info = self.get_info_json(e_uri)
        except:
            e = sys.exc_info()[0]
            print(e)

        if pool_info["loadBalancingMode"] == "fallback-ip":
            fip = True

        return fip

    def switch_fallback_ip(self, pool):
        '''
        Switches fallback IP to non-active member.
        Depends:
            get_member_ip_pool - returns get the IP for members of specified pool
            get_info_json - returns json for virtual servers

        :param pool:
            Required - must match name for GTM pool or will fail

        Returns None
        '''
        # Get current fallback ip
        e_uri = 'pool/~Common~{}'.format(pool)

        try:
            pool_info = self.get_info_json(e_uri)
        except:
            e = sys.exc_info()[0]

        c_fb_ip = pool_info['fallbackIpv4']

        # Get member ip
        m_ip = self.get_member_ip_pool(pool)

        # Set the uri for the REST POST
        f_uri = self.base_uri + e_uri

        # Set new fallback ip
        n_ip = [ip for ip in m_ip if not ip.split(':')[0] == c_fb_ip]

        print(n_ip, c_fb_ip)
        post = {'fallbackIpv4': n_ip[0].split(':')[0]}
        v = json.dumps(post)
        rev_req = self.session.put(f_uri, data=v, verify=False)
        print(f_uri, v)
        print(rev_req.status_code)
        print(rev_req.json())

    def get_member_vs_names(self, pool):
        '''
        Will get the member names of specified pool
        Depends:
            get_info_json - returns json of pool members

        :param pool:
            Required - must match name for GTM pool or will fail

        Returns dict of member names
        '''
        # Get pool info for members
        e_uri = 'pool/~Common~{}/members'.format(pool)

        try:
            p_info = self.get_info_json(e_uri)
        except:
            e = sys.exc_info()[0]
            print(e)

        # Get names for member servers
        m_srv = []
        for item in p_info['items']:
            m_srv.append(item['name'])

        return m_srv

    def get_member_ip_pool(self, pool):
        '''
        Will get the IP for members of specified pool.
        Depends:
            get_member_vsnames - returns list of virtual server names for pool
            then attaches to pull out the IP.
            get_info_json - returns json for virtual servers

        :param pool:
            Required - must match name for GTM pool or will fail

        Returns dict of ip addresses
        '''
        # Get member names
        p_mbr = self.get_member_vs_names(pool)

        # Get IP based on the names
        ip_addr = []
        for p_mem in p_mbr:
            f5_srv = p_mem.split(':')[0]
            vs = p_mem.split(':')[1]
            e_uri = 'server/~Common~{}/virtual-servers/{}'.format(f5_srv, vs)
            try:
                vs_info = self.get_info_json(e_uri)
            except:
                e = sys.exc_info()[0]
                print(e, "get_member_ip_pool")

            ip_addr.append(vs_info['destination'])

        return ip_addr
