# coding : utf-8
import json
import datetime
import time
import uuid
import os
from api.config import default_config
from api.utils import ensure_file
from api.models.cunik import Cunik


class CunikRegistry:
    """Local Cunik registry."""

    def __init__(self, registry_file):
        if registry_file:
            ensure_file(default_config.REGISTRY_ROOT, registry_file, content=json.dumps(dict()))
            self.registry_file = default_config.CUNIK_REGISTRY_FILE
            with open(self.registry_file) as fp:
                self._cuniks = self.convert_from_json(fp.read())
        else:
            self._cuniks = dict()

    @staticmethod
    def convert_from_json(s: str):
        d = {}
        for k, v in json.loads(s).items():
            w = Cunik.from_json(v)
            if w is not None:
                d[uuid.UUID(k)] = w
        return d

    def convert_to_json(self):
        d = {}
        for k, v in self._cuniks.items():
            w = v.to_json()
            if w is not None:
                d[str(k)] = w
        return d

    def save(self):
        if self.registry_file:
            with open(self.registry_file, 'w') as fp:
                json.dump(self.convert_to_json(), fp)

    def register(self, cunik):
        assert not self.query(cunik.uuid)
        cunik.create_time = time.time()
        self._cuniks[cunik.uuid] = cunik
        self.save()

    def remove(self, cunik):
        assert self.query(cunik.uuid)
        self._cuniks.pop(cunik.uuid)
        self.save()

    def populate(self, cunik):
        assert self.query(cunik.uuid)
        self._cuniks[cunik.uuid] = cunik
        self.save()

    def query(self, cid: uuid.UUID):
        return self._cuniks.get(uuid.UUID(cid))

    def get_id_list(self):
        return list(self._cuniks.keys())


cunik_registry = CunikRegistry(default_config.CUNIK_REGISTRY_FILE)
