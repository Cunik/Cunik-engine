import json
from os import path
from config import cunik_root


class DataVolumeRegistry:
    """The registry of data volumes.

    Usage:
        >>> dv = DataVolumeRegistry()
        >>> pt = dv.get_volume_path('test_volume')
    """
    def __init__(self):
        self.root = path.abspath(path.join(cunik_root, 'volumes'))
        with open(path.join(self.root, 'images.json'), 'r') as fp:
            self.volumes = json.load(fp)

    def get_volume_path(self, name: str):
        return path.join(self.root, self.volumes[name])


data_volume_registry = DataVolumeRegistry()
