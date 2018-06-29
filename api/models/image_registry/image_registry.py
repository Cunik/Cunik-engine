import json
from os import path
from api.config import default_config


class ImageRegistry:
    """The registry of images.

    Usage:
        >>> ir = ImageRegistry()
        >>> pt = ir.get_image_path('nginx')
    """

    def __init__(self):
        self.root = path.abspath(path.join(default_config.CUNIK_ROOT, 'images'))
        with open(path.join(self.root, 'images.json'), 'r') as fp:
            self.images = json.load(fp)

    def get_image_path(self, name: str):
        path_to_image = path.join(self.root, self.images[name])
        return path_to_image


image_registry = ImageRegistry()
