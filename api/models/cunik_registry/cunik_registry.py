# coding : utf-8


class CunikRegistry:
    """Local cunik registry."""

    def __init__(self):
        self._cuniks = {}

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
