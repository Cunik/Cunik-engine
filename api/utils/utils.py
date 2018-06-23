# coding : utf-8

import os


def ensure_file(file, content=''):
    if not os.path.exists(file):
        os.makedirs(file)
    if not os.path.getsize(file):
        with open(file, 'w') as f:
            f.write(content)
