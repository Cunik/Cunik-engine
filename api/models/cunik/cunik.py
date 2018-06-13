"""class Cunik."""

# from api.models.image_registry import image_registry
# from api.models.data_volume_registry import data_volume_registry
from backend.vm import VM, VMConfig
import uuid
import json


class CunikConfig:
    """Config of a cunik, constructed when the user wants to create a Cunik."""
    def __init__(self, **kwargs):
        self.name = kwargs['name']  # name of Cunik instance
        self.img = kwargs['img']  # path to image file
        self.cmd = kwargs['cmd']  # command line parameters
        self.vmm = kwargs['vmm']  # VM type
        self.mem = kwargs['mem']  # memory size in KB
        self.data_volume = kwargs['data_volume']  # data volume name

    def fill(path_to_cmdline: str, path_to_params: str):
        with open(path_to_cmdline) as f:
            cmdline = f.read()
        with open(path_to_params) as f:
            params = json.loads(f.read())
        list_of_cmdline = cmdline.split('"')
        list_of_cmdline = [params[p[2:-2]] if p[:2] == '{{' and p[-2:] == '}}' else p for p in list_of_cmdline]
        return '"'.join(list_of_cmdline)


class Cunik:
    """Represent a cunik.

    All the public methods of this class will immediately
    affect cunik registry and virtual machine unless it raises an exception.

    Usage:
        >>> cu = Cunik(...)  # Now there is a new cunik in cunik registry along with the vm instance
        >>> cu.start()  # Now it starts, and the new status is updated in cunik registry
        >>> cu.stop()
        >>> del cu  # NOTICE: This really destroys corresponding vm and remove this cunik from registry
    """
    def __init__(self, config: CunikConfig):
        """Initialize the cunik"""
        # Create the vm with the image
        self.id = uuid.uuid4()
        self.state = 'Not started'
        vmc = VMConfig()
        vmc.name = config.name
        vmc.image_path = config.img
        vmc.cmdline = config.cmd
        vmc.vdisk_path = config.data_volume
        vmc.hypervisor = config.vmm
        vmc.nic = 'tap0'
        vmc.memory_size = int(config.mem)
        print(vmc.name)
        print(vmc.image_path)
        print(vmc.cmdline)
        print(vmc.vdisk_path)
        print(vmc.hypervisor)
        print(vmc.nic)
        print(vmc.memory_size)
        self.vm = VM(vmc)
        # Register the cunik in the registry
        # CunikRegistry.register(xxx, self)

    def start(self):
        """Start the cunik."""
        # Start the vm
        self.vm.start()
        self.state = 'Running'
        # Update in registry
        # CunikRegistry.populate(xxx, self)

    def stop(self):
        """Stop the cunik."""
        # Stop the vm
        self.vm.stop()
        self.state = 'Stopped'
        # Update in registry
        # CunikRegistry.populate(xxx, self)

    def __del__(self):
        """Destroy a cunik according to the config."""
        # Destroy the vm
        del self.vm
        # Remove from registry
        # CunikRegistry.remove(xxx, self)
