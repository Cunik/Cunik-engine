# coding : utf-8

from api import create_app
from api.models import *
from flask_script import Manager

app = create_app('default')
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
