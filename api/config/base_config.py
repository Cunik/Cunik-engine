# coding : utf-8
import logging
import os
from logging.handlers import RotatingFileHandler


class BaseConfig:
    CUNIK_ROOT = os.path.realpath('/var/cunik/')
    LOG_FILE = os.path.realpath('/var/log/cunik.log')
    REGISTRY_ROOT = os.path.join(CUNIK_ROOT, '/registry/')
    CUNIK_REGISTRY_FILE = os.path.join(REGISTRY_ROOT, '/cunik.json')

    @staticmethod
    def init_app(app):
        handler = RotatingFileHandler(BaseConfig.LOG_FILE, maxBytes=10000, backupCount=1)
        handler.setLevel(logging.WARNING)
        app.logger.addHandler(handler)

