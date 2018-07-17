from os import path
from ..image import Image


class ImageRegistry:
    """The registry of images.

    Usage:
        >>> ir = ImageRegistry()
        >>> image = ir.get_image('nginx')
    """
    def __init__(self, root):
        self.root = root

    def get_image(self, name: str):
        return Image(root=path.join(self.root, name))
