# coding : utf-8

__all__ = ['configs', 'default_config']

from .dev_config import DevConfig
from .test_config import TestConfig

configs = {
    'default': DevConfig,
    'dev': DevConfig,
    'test': TestConfig
}

default_config = configs['default']