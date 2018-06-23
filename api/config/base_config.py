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

    CUNIK_FILE_ROOT = os.path.realpath('/var/cunik/')
    CUNIK_REGISTRY_FILE = os.path.join(CUNIK_FILE_ROOT, '/registry/cunik.json')

