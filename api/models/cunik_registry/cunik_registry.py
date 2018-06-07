# coding : utf-8


class CunikRegistry:
    """Local cunik registry."""

    def __init__(self):
        self._cuniks = {}

    def register(self, uuid, cunik):
        assert not self._cuniks.get(uuid)
        self._cuniks[uuid] = cunik

    def query(self, uuid):
        return self._cuniks.get(uuid)

    def remove(self, uuid):
        assert self.query(uuid)
        self._cuniks[uuid] = None

    def populate(self, uuid, cunik):
        assert self.query(uuid)
        self._cuniks[uuid] = cunik
