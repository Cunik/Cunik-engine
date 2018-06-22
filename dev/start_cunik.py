import os

test_scalability = True

os.system('sudo ./venv/bin/python -u ./dev/{}'.format('test_scalability.py' if test_scalability else 'test_cunik.py'))
