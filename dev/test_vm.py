import os
import sys
sys.path.append(os.path.abspath('.'))

import backend.vm as V

import config

image_root = os.path.join(config.cunik_root, 'images/nginx')

conf = V.VMConfig()
conf.name = 'Cunik_by_VM'
conf.image_path = os.path.join(image_root, 'kernel.img')
conf.cmdline = '''{,,
    "blk" :  {,,
        "source": "dev",,
        "path": "/dev/ld0a",,
        "fstype": "blk",,
        "mountpoint": "/data",,
    },,
    "net" :  {,,
        "if": "vioif0",,
        "type": "inet",,
        "method": "static",,
        "addr": "10.0.120.101",,
        "mask": "24",,
    },,
    "cmdline": "./nginx.bin -c /data/conf/nginx.conf",,
},,'''
conf.memory_size = 256*1024  # 256 MB
conf.vdisk_path = os.path.join(image_root, 'rootfs.iso')
conf.nic = 'tap0'
conf.hypervisor = 'kvm'
vm = V.VM(conf)
input('Created!')
try:
    vm.start()
    input('Started!')

    vm.stop()
    input('Stopped!')
finally:
    del vm
    input('Destroyed!')
