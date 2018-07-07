from backend.vm import VM
from os import path
import json
import sys
import os
import uuid
import backend.unikernel as uk


class CunikConfig:
    """Config of a cunik, constructed when the user wants to create a Cunik.

    Specifies:
        name *
        image *
        port *
        cmdline
    """
    def __init__(self, name, ipv4_addr, cmdline):
        self.name = name
        self.ipv4_addr = ipv4_addr
        self.cmdline = cmdline


class Cunik:
    """Represent a cunik, consists of image, vm and config.

    Usage:
        >>> cu = Cunik(...)  # Now there is a new cunik in cunik registry along with the vm instance
        >>> cu.start()  # Now it starts, and the new status is updated in cunik registry
        >>> cu.stop()
        >>> del cu  # NOTICE: This really destroys corresponding vm and remove this cunik from registry
    """
    def __init__(self, image, config: CunikConfig):
        """Initialize the cunik."""
        self.image = image
        self.config = config

        # Allocate resources, for now, only nic
        from ..nic_pool import nic_pool
        self.nic_name = nic_pool.alloc()

        vmc = uk.configure(image, config, nic_name=self.nic_name)
        # Then construct vm
        self.vm = VM(vmc)

    @property
    def uuid(self):
        return uuid.UUID(self.vm.uuid)

    @property
    def name(self):
        return self.vm.domain.name()

    @property
    def status(self):
        return self.vm.domain.state()

    def start(self):
        """Start the cunik."""
        # Start the vm
        self.vm.start()

    def stop(self):
        """Stop the cunik."""
        # Stop the vm
        self.vm.stop()

    def destroy(self):
        """Destroy a cunik according to the config."""
        # Destroy the vm
        self.vm.destroy()

    def to_json(self):
        return {'vm': self.vm.to_json()}


class CunikApi:
    pass