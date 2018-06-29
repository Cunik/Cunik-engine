import libvirt as lv
import xml.etree.cElementTree as ET
import sys, os


class InvalidVMConfigError(Exception):
    def __str__(self):
        return 'Invalid VM config, perhaps some vital parameters haven\'t been set.'


class UnknownHypervisorError(Exception):
    def __init__(self, hv):
        self.__hv = hv

    def __str__(self):
        return 'Unknown hypervisor {0}, not in {1}.'.format(self.__hv, VMConfig.available_hypervisors)


class VMConfig:
    """The handy representation of VM configuration.

    Usage:
        >>> vmc = VMConfig()  # A new VMConfig with default parameters, and key parameters are None
        >>> vmc.name = 'Cunik0'
        >>> vmc.kernel_path = './example.img'  # This has to be set
        >>> vmc.cmdline = './hello_world'  # Command line passed to kernel
        >>> vmc.memory_size = 1024  # Memory size in KB
        >>> vmc.vdisk_path = 'disk.iso'  # Virtual disk
        >>> vmc.nic = 'tap0'  # Network interface card
        >>> vmc.hypervisor = 'kvm'  # VM type
        >>> vmc.to_xml()  # Convert to XML for libvirt

    Usage(without standalone kernel):
        >>> vmc.system_image = './example.qcow'
    """
    available_hypervisors = ['kvm']

    def __init__(self):
        self.name = None
        self.kernel_path = None
        self.cmdline = None
        self.memory_size = 1024
        self.vdisk_path = None
        self.nic = None
        self.__hypervisor = None

    @property
    def hypervisor(self):
        return self.__hypervisor

    @hypervisor.setter
    def hypervisor(self, hv):
        """Set hypervisor type.

        Raises:
            UnknownHypervisorError
        """
        if hv not in self.available_hypervisors:
            raise UnknownHypervisorError
        self.__hypervisor = hv

    def __check(self):
        """Check if non-default parameters have been set.
            By non-default, I mean that it is None by default and have to be set before generation XML.
        """
        if not self.name:
            print('[ERROR] vm name not set', file=sys.stderr)
        if not self.hypervisor:
            print('[ERROR] vm hypervisor not set', file=sys.stderr)
        if not self.vdisk_path:
            print('[ERROR] vm vdisk path not set', file=sys.stderr)
        return all([self.name, self.vdisk_path, self.hypervisor])

    def to_xml(self):
        """Generate XML representation for libvirt.

        Raises:
            InvalidVMConfigError
        """
        if not self.__check():
            raise InvalidVMConfigError

        domain = ET.Element('domain')
        domain.set('type', self.hypervisor)

        name = ET.SubElement(domain, 'name')
        name.text = self.name

        os = ET.SubElement(domain, 'os')
        tp = ET.SubElement(os, 'type')
        tp.text = 'hvm'
        if self.kernel_path is not None:
            kernel = ET.SubElement(os, 'kernel')
            kernel.text = self.kernel_path
        if self.cmdline is not None:
            cmdline = ET.SubElement(os, 'cmdline')
            cmdline.text = 'console=ttyS0 ' + self.cmdline

        memory = ET.SubElement(domain, 'memory')
        memory.text = str(self.memory_size)

        # Disks
        devices = ET.SubElement(domain, 'devices')
        disk = ET.SubElement(devices, 'disk')
        disk.set('type', 'file')
        disk.set('device', 'disk')
        source = ET.SubElement(disk, 'source')
        source.set('file', self.vdisk_path)
        target = ET.SubElement(disk, 'target')
        target.set('dev', 'vda')
        target.set('bus', 'virtio')
        driver = ET.SubElement(disk, 'driver')
        # driver.set('type', 'raw')
        driver.set('name', 'qemu')
        readonly = ET.SubElement(disk, 'readonly')  # needed for qemu >= 2.10, for its image locking feature.

        # NIC
        # TODO: not recommended by libvirt
        ethernet = ET.SubElement(devices, 'interface')
        ethernet.set('type', 'ethernet')
        target = ET.SubElement(ethernet, 'target')
        target.set('dev', self.nic)
        model = ET.SubElement(ethernet, 'model')
        model.set('type', 'virtio')
        driver = ET.SubElement(ethernet, 'driver')
        driver.set('name', 'qemu')

        # Memballoon not supported, so none
        memballoon = ET.SubElement(devices, 'memballoon')
        memballoon.set('model', 'none')

        # For debugging
        serial = ET.SubElement(devices, 'serial')
        serial.set('type', 'pty')
        target = ET.SubElement(serial, 'target')
        target.set('port', '0')
        console = ET.SubElement(devices, 'console')
        console.set('type', 'pty')
        target = ET.SubElement(console, 'target')
        target.set('port', '0')
        target.set('type', 'serial')

        return ET.tostring(domain).decode()


class VM:
    """Refer to a vm.

    All the public methods of this class will immediately
    affect virtual machine unless it raises an exception.

    Usage:
        >>> vmc = VMConfig()
        >>> # ...
        >>> vm = VM(vmc)  # Now there is a new cunik in cunik registry along with the vm instance
        >>> uuid = vm.uuid  # Unique between all hosts, can be used to identify
        >>> vm.start()
        >>> vm.stop()
        >>> del vm  # Now this vm disappears
    """

    def __init__(self, config=None):
        # TODO: should we define then start or just create?
        if config is not None:
            if config.kernel_path is None or config.cmdline is None:
                self.config = config
                self.uuid = '75cb9413-13fd-457d-8e3c-d3dbc1102f80'
            else:
                conn = lv.open('')
                if conn is None:
                    print('[ERROR] Failed to open connection to qemu:///system', file=sys.stderr)
                self.domain = conn.defineXML(config.to_xml())
                self.uuid = self.domain.UUIDString()
                conn.close()
                self.config = None

    def start(self):
        """Start the vm, may raise exception."""
        if self.config is not None:
            cmd = '/usr/bin/qemu-system-x86_64 ' \
                  ' -enable-kvm -nographic -m 1024 ' \
                  ' -drive file={},if=virtio,cache=none,format=qcow2' \
                  ' -net tap,script=no,ifname={} -net nic,model=virtio >/dev/null 2>/dev/null &'.format(
                self.config.vdisk_path,
                self.config.nic
                )
            os.system(cmd)
        else:
            if self.domain.isActive():
                self.domain.resume()
            else:
                self.domain.create()

    def stop(self):
        # This is necessary because the vm may not be running
        if self.config is not None:
            return
        try:
                self.domain.suspend()
        except lv.libvirtError:
            pass

    def destroy(self):
        # This is necessary because the vm may not be running
        if self.config is not None:
            return
        try:
            self.domain.destroy()
        except lv.libvirtError:
            pass
        finally:
            self.domain.undefine()

    @staticmethod
    def from_json(vm_json: dict):
        res = VM()
        res.uuid = vm_json['uuid']
        conn = lv.open('')
        if conn is None:
            print('[ERROR] Failed to open connection to qemu:///system', file=sys.stderr)
        try:
            res.domain = conn.lookupByUUIDString(res.uuid)
        except lv.libvirtError:
            print('[ERROR] VM instance with UUID={} not found'.format(res.uuid), file=sys.stderr)
            raise KeyError
        if res.domain is None:
            print('[ERROR] Failed to find the domain with UUID={}'.format(res.uuid), file=sys.stderr)
        conn.close()
        return res

    def to_json(self):
        return {'uuid': self.uuid}
