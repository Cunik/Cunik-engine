from .nic_pool import NICPool
from api.config import default_config
import atexit

nic_pool = NICPool(default_config.SUBNET)


def exit_handler():
    nic_pool.release()


atexit.register(exit_handler)
