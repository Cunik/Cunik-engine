"""class Image."""


import json
from os import path


class Image:
    def __init__(self, root):
        self.root = root

        # Load json and fill meta information
        with open(path.join(self.root, 'metadata.json')) as f:
            metadata = json.load(f)

        # Fill main information
        self.name = metadata['name']
        self.unikernel = metadata['unikernel']['name']
        self.default_cmdline = metadata['default_cmdline']
