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

    """
    def __init__(self, name, nic_name=None, kernel_path=None, cmdline=None,
                 num_cpus=1, memory_size=4096, vdisk_path=None, vdisk_format='raw',
                 hypervisor='kvm'):
        self.name = name
        self.kernel_path = kernel_path
        self.cmdline = cmdline
        self.num_cpus = num_cpus
        self.memory_size = memory_size
        self.vdisk_path = vdisk_path
        self.vdisk_format = vdisk_format
        self.nic_name = nic_name
        self.hypervisor = hypervisor

    def to_xml(self):
        """Generate XML representation for libvirt.

        Raises:
            InvalidVMConfigError
        """
        domain = ET.Element('domain')
        domain.set('type', self.hypervisor)

        name = ET.SubElement(domain, 'name')
        name.text = self.name

        os = ET.SubElement(domain, 'os')
        tp = ET.SubElement(os, 'type')
        tp.text = 'hvm'
        if self.kernel_path:
            kernel = ET.SubElement(os, 'kernel')
            kernel.text = self.kernel_path
            cmdline = ET.SubElement(os, 'cmdline')
            cmdline.text = 'console=ttyS0 ' + self.cmdline

        vcpu = ET.SubElement(domain, 'vcpu')
        vcpu.set('placement', 'static')
        vcpu.text = str(self.num_cpus)

        memory = ET.SubElement(domain, 'memory')
        memory.text = str(self.memory_size)

        devices = ET.SubElement(domain, 'devices')

        # Disks
        if self.vdisk_path:
            disk = ET.SubElement(devices, 'disk')
            disk.set('type', 'file')
            disk.set('device', 'disk')
            source = ET.SubElement(disk, 'source')
            source.set('file', self.vdisk_path)
            target = ET.SubElement(disk, 'target')
            target.set('dev', 'vda')
            target.set('bus', 'virtio')
            driver = ET.SubElement(disk, 'driver')
            driver.set('type', self.vdisk_format)
            driver.set('name', 'qemu')
            # readonly = ET.SubElement(disk, 'readonly')  # needed for qemu >= 2.10, for its image locking feature.

        # NIC
        # TODO: not recommended by libvirt
        if self.nic_name:
            ethernet = ET.SubElement(devices, 'interface')
            ethernet.set('type', 'ethernet')
            target = ET.SubElement(ethernet, 'target')
            target.set('dev', self.nic_name)
            model = ET.SubElement(ethernet, 'model')
            model.set('type', 'virtio')
            driver = ET.SubElement(ethernet, 'driver')
            driver.set('name', 'qemu')

        # Memballoon not supported, so none
        memballoon = ET.SubElement(devices, 'memballoon')
        memballoon.set('model', 'none')

        # Features
        features = ET.SubElement(domain, 'features')
        acpi = ET.SubElement(features, 'acpi')

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
        conn = lv.open('')
        if conn is None:
            print('[ERROR] Failed to open connection to qemu:///system', file=sys.stderr)
        self.domain = conn.defineXML(config.to_xml())
        self.uuid = self.domain.UUIDString()
        conn.close()

    def start(self):
        """Start the vm, may raise exception."""
        if self.domain.isActive():
            self.domain.resume()
        else:
            self.domain.create()

    def stop(self):
        # This is necessary because the vm may not be running
        try:
            self.domain.suspend()
        except lv.libvirtError:
            pass

    def destroy(self):
        # This is necessary because the vm may not be running
        self.domain.undefine()
        try:
            self.domain.destroy()
        except:
            pass

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
