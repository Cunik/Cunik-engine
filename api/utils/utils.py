# coding : utf-8

import os


def ensure_file(directory, filename, content=''):
    if not os.path.isdir(directory):
        os.makedirs(directory)
    if not os.path.exists(filename):
        open(os.path.join(directory, filename), 'w').close()
    if not os.path.getsize(os.path.join(directory, filename)):
        with open(os.path.join(directory, filename), 'w') as f:
            f.write(content)
