# coding : utf-8
import json
import datetime
import time
import uuid
from api.config import default_config
from api.utils import ensure_file


class CunikRegistry:
    """Local Cunik registry."""

    def __init__(self, registry_file):
        if registry_file:
            self.registry_file = registry_file
            ensure_file(registry_file, content=json.dumps(dict()))
            self._cuniks = json.load(registry_file)
        else:
            self._cuniks = dict()

    def save(self):
        if self.registry_file:
            json.dump(self._cuniks, self.registry_file)

    def register(self, cunik):
        assert not self.query(cunik.id)
        cunik.create_time = time.time()
        self._cuniks[cunik.id] = cunik
        self.save()

    def remove(self, cunik):
        assert self.query(cunik.id)
        self._cuniks.pop(cunik.id)
        self.save()

    def populate(self, cunik):
        assert self.query(cunik.id)
        self._cuniks[cunik.id] = cunik
        self.save()

    def query(self, cid: uuid.UUID):
        return self._cuniks.get(cid)

    def get_id_list(self):
        return list(self._cuniks.keys())


cunik_registry = CunikRegistry(default_config.CUNIK_REGISTRY_FILE)
