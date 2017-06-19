import json
import f5


class GTMUtils(F5):

    def __init__(self, server, use_cache=False, **kwargs):
        self.name = self
        self.use_cache = use_cache
        super(GTMUtils, self).__init__()

    def set_gtm_pool(self):
        pass

    def get_gtm_pool(self):
        pass
