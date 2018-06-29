import json
from os import path
from api.config import default_config


class DataVolumeRegistry:
    """The registry of data volumes.

    Usage:
        >>> dv = DataVolumeRegistry()
        >>> pt = dv.get_volume_path('test_volume')
    """

    def __init__(self):
        self.root = path.abspath(path.join(default_config.CUNIK_ROOT, 'volumes'))
        with open(path.join(self.root, 'metadata.json'), 'r') as fp:
            self.volumes = json.load(fp)

    def add_volume_path(self, volume_name: str, volume_path: str):
        if self.volumes.get(volume_name):
            if self.volumes[volume_name] == volume_path:
                # volume path already added
                pass
            else:
                print('volume name conflict')
            return
        self.volumes[volume_name] = volume_path

    def get_volume_path(self, volume_name: str):
        return path.join(self.root, self.volumes[volume_name])


data_volume_registry = DataVolumeRegistry()
