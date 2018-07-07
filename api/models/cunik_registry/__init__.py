from .cunik_registry import CunikRegistry
from api.config import default_config
import atexit
import os


cunik_registry = CunikRegistry(os.path.join(default_config.CUNIK_ROOT, 'cuniks'))


def exit_handler():
    cunik_registry.clear()


atexit.register(exit_handler)
