# coding : utf-8
import logging
from logging.handlers import RotatingFileHandler


class BaseConfig:

    @staticmethod
    def init_app(app):
        handler = RotatingFileHandler('cunik.log', maxBytes=10000, backupCount=1)
        handler.setLevel(logging.WARNING)
        app.logger.addHandler(handler)
