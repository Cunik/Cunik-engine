# coding : utf-8

from api import create_app
from api.models import *
from flask_script import Manager
from tests import TestAll

app = create_app('default')
manager = Manager(app)

manager.add_command('test', TestAll())

if __name__ == '__main__':
    manager.run()
