# coding : utf-8
import json
import datetime
import time
import uuid
import os
from api.config import BaseConfig
from api.utils import ensure_file
from api.models.cunik import Cunik


class CunikRegistry:
    """Local Cunik registry."""

    def __init__(self, registry_file):
        if registry_file:
            ensure_file(BaseConfig.REGISTRY_ROOT, registry_file, content=json.dumps(dict()))
            self.registry_file = BaseConfig.CUNIK_REGISTRY_FILE
            with open(self.registry_file) as fp:
                self._cuniks = self.convert_from_json(fp.read())
        else:
            self._cuniks = dict()

    def convert_from_json(self, s: str):
        return {uuid.UUID(k): Cunik.from_json(v) for k, v in json.loads(s).items()}

    def convert_to_json(self):
        return {str(k): v.to_json() for k, v in self._cuniks.items()}

    def save(self):
        if self.registry_file:
            with open(self.registry_file, 'w') as fp:
                json.dump(self.convert_to_json(), fp)

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


cunik_registry = CunikRegistry(BaseConfig.CUNIK_REGISTRY_FILE)
