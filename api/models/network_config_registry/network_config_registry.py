import json
from os import path

from api.config import default_config


class NetworkConfigRegistry:
    """The registry of network configurations.

    Usage:
        >>> nc = NetworkConfigRegistry()
        >>> pt = nc.get_config_path('test_networkconfig')
    """
    def __init__(self):
        self.root = path.abspath(path.join(default_config.CUNIK_ROOT, 'networkconfigs'))
        with open(path.join(self.root, 'metadata.json'), 'r') as fp:
            self.configs = json.load(fp)

    def get_config_path(self, name: str):
        return path.join(self.root, self.configs[name])


network_config_registry = NetworkConfigRegistry()
