"""class Cunik."""

# from api.models.image_registry import image_registry
# from api.models.data_volume_registry import data_volume_registry
from backend.vm import VM, VMConfig
import uuid
import json


class CunikConfig:
    """Config of a cunik, constructed when the user wants to create a Cunik."""
    def __init__(self, **kwargs):
        vital_keys_set = {'name', 'image', 'cmdline', 'hypervisor', 'memory', 'data_volume'}
        all_keys_set = set.union(vital_keys_set, set())
        if not set(kwargs.keys()) <= all_keys_set:
            raise KeyError(list(set(kwargs.keys()) - all_keys_set)[0] +
                           ' is an invalid keyword argument for this function')
        if not set(kwargs.keys()) >= vital_keys_set:
            raise KeyError(list(vital_keys_set - set(kwargs.keys()))[0] +
                           ' is a vital keyword argument for this function but has not been set')
        self.name = kwargs['name']  # name of Cunik instance
        self.image = kwargs['image']  # path to image file
        self.cmdline = kwargs['cmdline']  # command line parameters
        self.hypervisor = kwargs['hypervisor']  # VM type
        try:
            self.memory = int(kwargs['memory'])  # memory size in KB
            if self.memory <= 0:
                raise ValueError('memory size must be an positive integer')
        except ValueError:
            raise ValueError('memory size must be an integer')
        self.data_volume = kwargs['data_volume']  # data volume name

    @staticmethod
    def fill(path_to_cmdline: str, path_to_params: str):
        try:
            with open(path_to_cmdline) as f:
                cmdline = f.read()
        except IOError as IE:
            raise IOError('cmdline file not found: {0}'.format(IE))
        try:
            with open(path_to_params) as f:
                try:
                    params = json.loads(f.read())
                except ValueError as VE:
                    raise ValueError('{0} is not a valid json file: {1}'.format(path_to_params, VE))
        except IOError as IE:
            raise IOError('params file not found: {0}'.format(IE))
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
        vmc.image_path = config.image
        vmc.cmdline = config.cmdline
        vmc.vdisk_path = config.data_volume
        vmc.hypervisor = config.hypervisor
        vmc.nic = 'tap0'
        vmc.memory_size = int(config.memory)
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
