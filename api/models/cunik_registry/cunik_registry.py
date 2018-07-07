# coding : utf-8
import json
import time
import uuid
import shutil
from api.models.cunik import Cunik, CunikConfig


class CunikRegistry:
    """Local Cunik registry."""
    def __init__(self, root):
        self.root = root
        self._cuniks = dict()

    def create(self, name, image_name, ipv4_addr, cmdline=None):
        cfg = CunikConfig(name=name, ipv4_addr=ipv4_addr, cmdline=cmdline)

        from ..image_registry import image_registry
        image = image_registry.get_image(image_name)  # TODO: no error handling for now

        cu = Cunik(image, cfg)
        self.register(cu)
        cu.start()

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

    def commit(self):
        pass

    def register(self, cunik: Cunik):
        assert not self.query(cunik.uuid)
        cunik.create_time = time.time()
        self._cuniks[cunik.uuid] = cunik
        self.commit()

    def remove(self, cunik):
        assert self.query(cunik.uuid)
        self._cuniks.pop(cunik.uuid)
        self.commit()

    def populate(self, cunik):
        assert self.query(cunik.uuid)
        self._cuniks[cunik.uuid] = cunik
        self.commit()

    def query(self, cid: uuid.UUID):
        if isinstance(cid, str):
            cid = uuid.UUID(cid)
        return self._cuniks.get(cid)

    def get_id_list(self):
        return list(self._cuniks.keys())

    def clear(self):
        for cu in self._cuniks.values():
            cu.destroy()
        self._cuniks.clear()
        try:
            shutil.rmtree(self.root)
        except FileNotFoundError:
            pass
