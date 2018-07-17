from .image_registry import ImageRegistry
from api.config import default_config
import os

image_registry = ImageRegistry(os.path.join(default_config.CUNIK_ROOT, 'images'))
