"""class Cunik."""

# from api.models.image_registry import image_registry
# from api.models.data_volume_registry import data_volume_registry
from backend.vm import VM, VMConfig
import uuid
import json


class CunikApi:

    @staticmethod
    def create(image_name, params=None):
        """
        Create a new cunik.

        Usage:
            >>> cunik = CunikApi.create('nginx', {'ipv4_addr': '10.0.20.1'})
            >>> print(cunik["uuid"])
        """
        pass

    @staticmethod
    def list():
        """
        Return all created cunik and its simple information.
        Usage:
            >>> cuniks = CunikApi.list()
            >>> for cunik in cuniks:
            >>>     print(cunik["uuid"])
            >>>     print(cunik["create_time"])
            >>>     print(cunik["image_name"])
        """
        return []

    @staticmethod
    def info(uuid):
        """
        Return all informations about a cunik.
        Usage:
            >>> uuid = 'acb123'
            >>> cunik = CunikApi.info(uuid)
            >>> print(cunik["uuid"])
            >>> print(cunik["create_time"])
            >>> print(cunik["image_name"])
            >>> print(cunik["params"])
            >>> print(cunik["params"]["ipv4_addr"])
        """
        return {}


    @staticmethod
    def stop(uuid):
        """
        Stop a running cunik.
        Usage:
            >>> uuid = 'acb123'
            >>> CunikApi.stop(uuid)
        """
        return None

    @staticmethod
    def remove(uuid):
        """
        (Stop and) Remove a created cunik.
        Usage:
            >>> uuid = 'acb123'
            >>> CunikApi.remove(uuid)
        """
        return None

class CunikConfig:
    """Config of a cunik, constructed when the user wants to create a Cunik."""
    def __init__(self, **kwargs):
        vital_keys_set = {'name', 'image', 'cmdline', 'hypervisor', 'memory', 'data_volume'}
        all_keys_set = set.union(vital_keys_set, {'nic'})
        if not set(kwargs.keys()) <= all_keys_set:
            raise KeyError('[ERROR] ' + list(set(kwargs.keys()) - all_keys_set)[0] +
                           ' is an invalid keyword argument for this function')
        if not set(kwargs.keys()) >= vital_keys_set:
            raise KeyError('[ERROR] ' + list(vital_keys_set - set(kwargs.keys()))[0] +
                           ' is a vital keyword argument for this function but has not been set')
        self.name = kwargs.get('name')  # name of Cunik instance
        self.image = kwargs.get('image')  # path to image file
        self.cmdline = kwargs.get('cmdline')  # command line parameters
        self.hypervisor = kwargs.get('hypervisor')  # VM type
        self.nic = kwargs.get('nic')
        try:
            self.memory = int(kwargs['memory'])  # memory size in KB
        except ValueError as VE:
            print('[ERROR] memory size must be an integer')
            raise VE
        try:
            assert self.memory > 0
        except AssertionError as AE:
            print('[ERROR] memory size must be a positive integer')
            raise AE
        self.data_volume = kwargs['data_volume']  # data volume name

    @staticmethod
    def fill(path_to_cmdline: str, path_to_params: str, **kwargs):
        try:
            with open(path_to_cmdline) as f:
                cmdline = f.read()
        except IOError as IE:
            print('[ERROR] cmdline file not found: {0}'.format(IE))
            raise IE
        try:
            with open(path_to_params) as f:
                params = json.loads(f.read())
        except ValueError as VE:
            print('[ERROR] {0} is not a valid json file: {1}'.format(path_to_params, VE))
            raise VE
        except IOError as IE:
            print('[ERROR] params file not found: {0}'.format(IE))
            raise IE
        params.update(kwargs)
        list_of_cmdline = cmdline.split('"')
        try:
            list_of_cmdline = [params[p[2:-2]] if p[:2] == '{{' and p[-2:] == '}}' else p for p in list_of_cmdline]
        except KeyError as KE:
            print('[ERROR] params in cmdline not filled: {0}'.format(KE))
            raise KE
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
        vmc.nic = config.nic
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
