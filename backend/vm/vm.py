import libvirt as lv
import xml.etree.cElementTree as ET


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
        >>> vmc.image_path = './example.img'  # This has to be set
        >>> vmc.memory_size = 1024  # Memory size in KB
        >>> vmc.hypervisor = 'kvm'  # VM type
        >>> vmc.to_xml()  # Convert to XML for libvirt
    """
    available_hypervisors = ['kvm']

    def __init__(self):
        self.name = None
        self.image_path = None
        self.cmdline = ''
        self.memory_size = 1024
        self.__hypervisor = None
        self.data_volume_path = None
        self.data_volume_mount_point = None
        self.network_config = None

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
        return all([self.name, self.image_path, self.hypervisor, self.data_volume_path, self.data_volume_mount_point,
                    self.network_config])

    @property
    def to_xml(self):
        """Generate XML representation for libvirt.

        Raises:
            InvalidVMConfigError
        """
        if not self.__check():
            raise InvalidVMConfigError

        domain = ET.Element('domain')
        domain.set('type', 'kvm')

        name = ET.SubElement(domain, 'name')
        name.text = self.name

        os = ET.SubElement(domain, 'os')
        tp = ET.SubElement(os, 'type')
        tp.text = 'hvm'
        kernel = ET.SubElement(os, 'kernel')
        kernel.text = self.image_path
        cmdline = ET.SubElement(os, 'cmdline')
        cmdline.text = 'console=ttyS0' + ('''{,,
            "blk" :  {,,
                "source": "dev",,
                "path": "/dev/ld0a",,  
                "fstype": "blk",,
                "mountpoint": "%s",,
            },,
            "net" :  {,,
                "if": "vioif0",, 
                "type": "inet",,
                "method": "static",,
                "addr": "10.0.120.101",,
                "mask": "24",, 
            },,
            "cmdline": "%s",,  
        },,''' % (self.data_volume_mount_point, self.cmdline))

        memory = ET.SubElement(domain, 'memory')
        memory.text = str(self.memory_size)

        # Disks
        devices = ET.SubElement(domain, 'devices')
        disk = ET.SubElement(devices, 'disk')
        disk.set('type', 'file')
        disk.set('device', 'disk')
        source = ET.SubElement(disk, 'source')
        source.set('file', self.data_volume_path)
        target = ET.SubElement(disk, 'target')
        target.set('dev', 'vda')
        target.set('bus', 'virtio')
        driver = ET.SubElement(disk, 'driver')
        driver.set('type', 'raw')
        driver.set('name', 'qemu')

        # NIC
        # TODO: not recommended by libvirt
        ethernet = ET.SubElement(devices, 'interface')
        ethernet.set('type', 'ethernet')
        target = ET.SubElement(ethernet, 'target')
        target.set('dev', 'tap0')
        model = ET.SubElement(ethernet, 'model')
        model.set('type', 'virtio')
        driver = ET.SubElement(ethernet, 'driver')
        driver.set('name', 'qemu')

        # Memballoon not supported, so none
        memballoon = ET.SubElement(devices, 'memballoon')
        memballoon.set('model', 'none')

        # For debugging
        # TODO: add console option
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
    def __init__(self, config: VMConfig):
        # TODO: should we define then start or just create?
        conn = lv.open('')  # TODO: set URI by vm type
        self.domain = conn.defineXML(config.to_xml)
        self.uuid = self.domain.UUIDString()
        conn.close()

    def start(self):
        """Start the vm, may raise exception."""
        if self.domain.isActive():
            self.domain.resume()
        else:
            self.domain.create()

    def stop(self):
        self.domain.suspend()

    def __del__(self):
        # This is necessary because the vm may not be running
        try:
            self.domain.destroy()
        finally:
            self.domain.undefine()
