# coding : utf-8
import logging
import os
from logging.handlers import RotatingFileHandler


class BaseConfig:
    CUNIK_ROOT = os.path.realpath('/var/cunik')
    LOG_FILE = os.path.realpath('/var/log/cunik.log')
    REGISTRY_ROOT = os.path.join(CUNIK_ROOT, 'registry')
    BRIDGE_NAME = 'cunik'
    SUBNET = '10.0.125.0/24'

    @staticmethod
    def init_app(app):
        pass
