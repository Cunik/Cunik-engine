import libvirt as lv
import xml.etree.cElementTree as ET


class VMConfig:
    pass


class VM:
    """Represent a vm.

    All the public methods of this class will immediately
    affect virtual machine unless it raises an exception.

    Usage:
        >>> vm = VM(...)  # Now there is a new cunik in cunik registry along with the vm instance
    """
    def __init__(self, config):
        conn = lv.open('')
        self.domain = conn.defineXML(self.__gen_xml(config))

    def start(self):
        """Start the vm, may raise exception."""
        self.domain.create()  # Or resume, later

    def stop(self):
        self.domain.suspend()

    def destroy(self):
        try:
            self.domain.destroy()
        finally:
            self.domain.undefine()

    @staticmethod
    def __gen_xml(config):
        domain = ET.Element('domain')
        domain.set('type', 'kvm')

        name = ET.SubElement(domain, 'name')
        name.text = config.name

        os = ET.SubElement(domain, 'os')
        tp = ET.SubElement(os, 'type')
        tp.text = 'hvm'
        kernel = ET.SubElement(os, 'kernel')
        kernel.text = config.image
        cmdline = ET.SubElement(os, 'cmdline')
        cmdline.text = config.cmd

        memory = ET.SubElement(domain, 'memory')
        memory.text = '100'

        return ET.tostring(domain).decode()
