import json
from os import path
from config import cunik_root


class ImageRegistry:
    """The registry of data volumes.

    Usage:
        >>> ir = ImageRegistry()
        >>> pt = ir.get_image_path('nginx')
    """
    def __init__(self):
        self.root = path.abspath(path.join(cunik_root, 'images'))
        with open(path.join(self.root, 'metadata.json'), 'r') as fp:
            self.images = json.load(fp)

    def get_image_path(self, name: str):
        return path.join(self.root, self.images[name])


image_registry = ImageRegistry()
