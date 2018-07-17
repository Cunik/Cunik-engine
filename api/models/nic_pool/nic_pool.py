import pyroute2 as pr
from api.config import default_config


class NICPool:
    """NICPool.

    Use pyroute2.IPDB to manage interfaces, and memorizes the objects created.
    """
    def __init__(self, subnet):
        self.ipdb = pr.IPDB()
        self.bridge = self.ipdb.create(
            kind='bridge',
            ifname=default_config.BRIDGE_NAME
        ).add_ip(default_config.SUBNET).up().commit()
        self.nics = {}

    def alloc(self):
        # Pick a name and create the tap device
        nicname = 'cunik_tap{}'.format(len(self.nics))
        nic = self.ipdb.create(kind='tuntap', mode='tap', ifname=nicname).commit()
        self.bridge.add_port(nic).commit()
        self.nics[nicname] = nic
        return nicname

    def free(self, nicname):
        # Destroy the tap device
        self.nics[nicname].down().remove().commit()
        self.nics.pop(nicname)

    def release(self):
        for n in self.nics.values():
            n.down().remove()
        self.bridge.down().remove()
        self.ipdb.commit().release()
