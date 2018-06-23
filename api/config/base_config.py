# coding : utf-8
import logging
import os
from logging.handlers import RotatingFileHandler


class BaseConfig:

    @staticmethod
    def init_app(app):
        handler = RotatingFileHandler('cunik.log', maxBytes=10000, backupCount=1)
        handler.setLevel(logging.WARNING)
        app.logger.addHandler(handler)

    CUNIK_ROOT = os.path.realpath('/var/cunik/')
    REGISTRY_ROOT = os.path.join(CUNIK_ROOT, '/registry/')
    CUNIK_REGISTRY_FILE = os.path.join(REGISTRY_ROOT, '/cunik.json')

