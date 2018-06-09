# coding : utf-8
import json
from config import cunik_root


class CunikRegistry:
    """Local cunik registry."""

    def __init__(self, Regfile):
        self._cuniks = json.load(Regfile)

    def register(self, cunik):
        assert not self.query(cunik.id)
        self._cuniks[cunik.id] = cunik

    def query(self, id):
        return self._cuniks.get(id)

    def remove(self, cunik):
        assert self.query(cunik.id)
        self._cuniks[cunik.id].pop(cunik.id)

    def populate(self, cunik):
        assert self.query(cunik.id)
        self._cuniks[cunik.id] = cunik


# cunik_registry = CunikRegistry(Regfile)