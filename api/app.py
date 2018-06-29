# coding : utf-8

from flask import Flask
from .config import configs


def create_app(config_name='default'):
    app = Flask(__name__)
    config_obj = configs.get(config_name)
    app.config.from_object(config_obj)
    config_obj.init_app(app)

    # register bps
    from .router import routes

    for r in routes:
        print('register bp with prefix: {}' % r.prefix)
        app.register_blueprint(r.bp, url_prefix=r.prefix)

    return app

