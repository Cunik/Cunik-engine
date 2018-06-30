"""class Cunik."""

from api.models.image_registry import image_registry
from api.models.data_volume_registry import data_volume_registry
from backend.vm import VM, VMConfig
from os import path
from api.config import default_config
import json
import sys
import os
import uuid
import re


class CunikConfig:
    """Config of a cunik, constructed when the user wants to create a Cunik."""

    def __init__(self, **kwargs):
        vital_keys_set = {'name', 'image', 'hypervisor', 'memory'}
        all_keys_set = set.union(vital_keys_set, {'nic', 'data_volume', 'cmdline'})
        if not set(kwargs.keys()) <= all_keys_set:
            raise KeyError('[ERROR] ' + list(set(kwargs.keys()) - all_keys_set)[0] +
                           ' is an invalid keyword argument for this function')
        if not set(kwargs.keys()) >= vital_keys_set:
            raise KeyError('[ERROR] ' + list(vital_keys_set - set(kwargs.keys()))[0] +
                           ' is a vital keyword argument for this function but has not been set')
        # name of Cunik instance
        self.name = kwargs.get('name')
        # path to image file
        try:
            self.image = image_registry.get_image_path(kwargs.get('image'))
        except KeyError as KE:
            print('[ERROR] cannot find image {} in registry'.format(kwargs['image']), file=sys.stderr)
            raise KE
        # command line parameters
        self.cmdline = kwargs.get('cmdline')
        # VM type
        self.hypervisor = kwargs.get('hypervisor')
        self.nic = kwargs.get('nic')
        # memory size in KB
        try:
            self.memory = int(kwargs['memory'])
        except ValueError as VE:
            print('[ERROR] memory size must be an integer', file=sys.stderr)
            raise VE
        try:
            assert self.memory > 0
        except AssertionError as AE:
            print('[ERROR] memory size must be a positive integer', file=sys.stderr)
            raise AE
        # data volume name
        if kwargs.get('data_volume'):
            try:
                self.data_volume = data_volume_registry.get_volume_path(kwargs['data_volume'])
            except KeyError as KE:
                print('[ERROR] cannot find data volume {} in registry'.format(kwargs['data_volume']), file=sys.stderr)
                raise KE

    @staticmethod
    def fill(path_to_cmdline: str, path_to_params: str, **kwargs):
        try:
            with open(path.join(default_config.CUNIK_ROOT, path_to_cmdline)) as f:
                cmdline = f.read()
        except IOError as IE:
            print('[ERROR] cmdline file not found: {0}'.format(IE), file=sys.stderr)
            raise IE
        try:
            with open(path.join(default_config.CUNIK_ROOT, path_to_params)) as f:
                params = json.loads(f.read())
        except ValueError as VE:
            print('[ERROR] {0} is not a valid json file: {1}'.format(path_to_params, VE), file=sys.stderr)
            raise VE
        except IOError as IE:
            print('[ERROR] params file not found: {0}'.format(IE), file=sys.stderr)
            raise IE
        params.update(kwargs)
        for k, v in params.items():
            cmdline = cmdline.replace('{{' + k + '}}', v)
        return cmdline


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

    def __init__(self, config=None):
        """Initialize the cunik"""

        if config is not None:
            self.state = 'Not started'
            vmc = VMConfig()
            vmc.name = config.name
            vmc.kernel_path = config.image
            vmc.cmdline = config.cmdline
            vmc.vdisk_path = config.data_volume
            vmc.hypervisor = config.hypervisor
            vmc.nic = config.nic
            vmc.memory_size = int(config.memory)
            self.vm = VM(vmc)
            # Register the cunik in the registry
            from api.models.cunik_registry import cunik_registry
            cunik_registry.register(self)

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
        # Update in registry
        from api.models.cunik_registry import cunik_registry
        cunik_registry.populate(self)

    def stop(self):
        """Stop the cunik."""
        # Stop the vm
        self.vm.stop()
        # Update in registry
        from api.models.cunik_registry import cunik_registry
        cunik_registry.populate(self)

    def destroy(self):
        """Destroy a cunik according to the config."""
        # Destroy the vm
        self.vm.destroy()
        # Remove from registry
        from api.models.cunik_registry import cunik_registry
        cunik_registry.remove(self)

    def to_json(self):
        return {'vm': self.vm.to_json()}

    @staticmethod
    def from_json(cunik_json: dict):
        res = Cunik()
        try:
            res.vm = VM.from_json(cunik_json['vm'])
        except KeyError:
            print('[ERROR] Cunik registry data error', file=sys.stderr)
            return None
        return res


class CunikApi:

    @staticmethod
    def create(image_name, params=None, **kwargs):
        """
        Create a new cunik.

        Usage:
            >>> cunik = CunikApi.create('nginx', {'ipv4_addr': '10.0.20.1'})
            >>> print(cunik["id"])
        """

        def mex(name: str, names: set) -> int:
            i = 1
            while name + str(i) in names:
                i += 1
            return i

        def trans(ipv4):
            list_of_ipv4 = ipv4.split('.')
            list_of_ipv4[-1] = '100'
            return '.'.join(list_of_ipv4)

        if not params:
            params = {}
        with open(path.join(default_config.CUNIK_ROOT, 'images', image_name, 'config.json')) as f:
            default_conf = json.load(f)
        cmdline = None
        with open(path.join(default_config.CUNIK_ROOT, 'images', image_name, 'metadata.json')) as f:
            metadata = json.load(f)
            try:
                unikernel_type = metadata['unikernel']['name']
            except KeyError:
                raise KeyError
            else:
                if unikernel_type == 'osv':
                    from backend.unikernel.osv import preprocess
                    # empty
                elif unikernel_type == 'rumprun':
                    from backend.unikernel.rumprun import preprocess
                    # cmdline
                else:
                    print('Unsupported Unikernel type', file=sys.stderr)
                    raise ValueError
                cmdline = CunikConfig.fill('images/{}/cmdline'.format(image_name),
                                           'images/{}/params.json'.format(image_name), **params)
                cmdline = preprocess(path.join(default_config.CUNIK_ROOT, 'images', image_name), cmdline)
        if cmdline is not None:
            default_conf['cmdline'] = cmdline
        if default_conf.get('data_volume'):
            if not params.get('data_volume'):
                default_conf['data_volume'] = '{}_default'.format(image_name)
            else:
                default_conf['data_volume'] = params['data_volume']
        else:
            default_conf['data_volume'] = image_name + '_default'
        image_name_set = {json.loads(CunikApi.info(i))['name'] for i in CunikApi.list()}
        image_name_index = mex(image_name, image_name_set)
        tap_name_set = {i[:-1] for i in os.popen('ifconfig').read().split() if i[-1] == ':'}
        tap_name_index = mex('tap', tap_name_set)
        tap_device_name = 'tap{}'.format(tap_name_index)
        if params.get('ipv4_addr'):
            os.system('ip l del {} 2>/dev/null'.format(tap_device_name))
            os.system('ip tuntap add {} mode tap'.format(tap_device_name))
            os.system('ip addr add {}/24 dev {}'.format(trans(params['ipv4_addr']), tap_device_name))
            os.system('ip link set dev {} up'.format(tap_device_name))
        cfg = CunikConfig(
            name=image_name + str(image_name_index),
            image=image_name,
            nic=tap_device_name,
            **default_conf
        )
        Cunik(cfg).start()

    @staticmethod
    def list():
        """
        Return all created cunik and its simple information.
        Usage:
            >>> cuniks = CunikApi.list()
            >>> for cunik in cuniks:
            >>>     print(cunik["id"])
            >>>     print(cunik["create_time"])
            >>>     print(cunik["name"])
        """
        from api.models.cunik_registry import cunik_registry
        return list(map(str, cunik_registry.get_id_list()))

    @staticmethod
    def info(cid):
        """
        Return all informations about a cunik.
        Usage:
            >>> id = 'acb123'
            >>> cunik = CunikApi.info(id)
            >>> print(cunik["id"])
            >>> print(cunik["create_time"])
            >>> print(cunik["name"])
            >>> print(cunik["params"])
            >>> print(cunik["params"]["ipv4_addr"])
        """
        from api.models.cunik_registry import cunik_registry
        cunik = cunik_registry.query(cid)
        cunik_info = {}
        if cunik is not None:
            cunik_info["uuid"] = str(cunik.uuid)
            cunik_info["name"] = cunik.name
            cunik_info["status"] = cunik.status
        return json.dumps(cunik_info)

    @staticmethod
    def stop(cid):
        """
        Stop a running cunik.
        Usage:
            >>> id = 'acb123'
            >>> CunikApi.stop(id)
        """
        from api.models.cunik_registry import cunik_registry
        cunik = cunik_registry.query(cid)
        if cunik is not None:
            cunik.stop()
            return 1
        else:
            return 0

    @staticmethod
    def start(cid):
        """
        Start a not running cunik.
        Usage:
            >>> id = 'acb123'
            >>> CunikApi.start(id)
        """
        from api.models.cunik_registry import cunik_registry
        cunik = cunik_registry.query(cid)
        if cunik is not None:
            cunik.start()
            return 1
        else:
            return 0

    @staticmethod
    def remove(cid):
        """
        (Stop and) Remove a created cunik.
        Usage:
            >>> id = 'acb123'
            >>> CunikApi.remove(id)
        """
        from api.models.cunik_registry import cunik_registry
        cunik = cunik_registry.query(cid)
        if cunik is not None:
            cunik.destroy()
            return 1
        else:
            return 0
