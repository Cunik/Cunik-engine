# coding : utf-8

__all__ = ['configs']

from .dev_config import DevConfig
from .test_config import TestConfig

configs = {
    'default': DevConfig,
    'dev': DevConfig,
    'test': TestConfig
}
