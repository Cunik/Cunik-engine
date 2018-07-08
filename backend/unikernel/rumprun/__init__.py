"""Implements interface for Rumprun unikernels."""


from backend.vm import VMConfig
from os import path


class Rumprun:
    cmdline_template = '''{{,,
                "blk" :  {{,,
                    "source": "dev",,
                    "path": "/dev/ld0a",,
                    "fstype": "blk",,
                    "mountpoint": "/data",,
                }},,
                "net" :  {{,,
                    "if": "vioif0",,
                    "type": "inet",,
                    "method": "static",,
                    "addr": "{ipv4_addr}",,
                    "mask": "24",,
                }},,
                "cmdline": "{extra_cmdline}",,
            }},,
    '''

    @staticmethod
    def configure(image, config, nic_name):
        cmdline = Rumprun.cmdline_template.format(
            ipv4_addr=config.ipv4_addr,
            extra_cmdline=config.cmdline if config.cmdline else image.default_cmdline,
        )
        vmc = VMConfig(
            name=config.name,
            cmdline=cmdline,
            nic_name=nic_name,
            vdisk_path=path.join(image.root, 'data.iso'),
            memory_size=1024000
        )
        vmc.kernel_path = path.join(image.root, 'kernel.bin')
        return vmc
