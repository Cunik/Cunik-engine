"""Implements interface for OSv unikernels."""


from backend.vm import VMConfig
from os import path
from .imgedit import set_cmdline


class OSv:
    cmdline_template = "--ip=eth0,{ipv4_addr},255.255.255.0 --defaultgw=10.0.125.0 --nameserver=10.0.125.0 {extra_cmdline}"

    @staticmethod
    def configure(image, config, nic_name):
        cmdline = OSv.cmdline_template.format(
            ipv4_addr=config.ipv4_addr,
            extra_cmdline=config.cmdline if config.cmdline else image.default_cmdline,
        )
        set_cmdline(path.join(image.root, 'system.qemu'), cmdline)
        vmc = VMConfig(
            name=config.name,
            nic_name=nic_name,
            vdisk_path=path.join(image.root, 'system.qemu'),
            vdisk_format='qcow2',
            memory_size=1024000
        )
        return vmc
