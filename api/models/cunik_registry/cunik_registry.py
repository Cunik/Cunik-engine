# coding : utf-8
import json
import datetime
import time
import uuid
from config import cunik_root


class CunikRegistry:
    """Local cunik registry."""

    def __init__(self, regfile):
        if regfile:
            self._cuniks = json.load(regfile)
        else:
            self._cuniks = dict()

    def register(self, cunik):
        assert not self.query(cunik.id)
        cunik.create_time = time.time()
        self._cuniks[cunik.id] = cunik

    def query(self, cid: uuid.UUID):
        return self._cuniks.get(cid)

    def remove(self, cunik):
        assert self.query(cunik.id)
        self._cuniks.pop(cunik.id)

    def populate(self, cunik):
        assert self.query(cunik.id)
        self._cuniks[cunik.id] = cunik

    def get_id_list(self):
        return list(self._cuniks.keys())


cunik_registry = CunikRegistry(None)
