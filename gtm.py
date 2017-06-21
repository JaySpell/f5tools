import json
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
        pool_info = self._get_primary_pool_member(pool)

        # If pool info includes members switch 0 & 1 (reverse order)
        if pool_info is not None:

            # Reverse member 1 & member 2
            pool_post = {
                pool_info['s_link']: {"member": 0},
                pool_info['p_link']: {"member": 1}
            }

            # Sent command to reverse
            for k, v in pool_post.items():
                #rev_req = self.session.put(k, data=v, verify=False)
                print(k, v)

    def get_gtm_pool(self):
        pass

    def _get_primary_pool_member(self, pool):
        '''
        Will return the active site for a pool based on global availability
        '''

        # Set query URI
        e_uri = 'pool/~Common~{}/members'.format(pool)
        full_uri = self.base_uri + e_uri
        s_link = None
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

        return pool_info
