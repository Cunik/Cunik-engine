import os
import sys
sys.path.append(os.path.abspath('.'))

import backend.vm as V

from api.config import default_config

images_root = os.path.join(default_config.CUNIK_ROOT, 'images/nginx')
volumes_root = os.path.join(default_config.CUNIK_ROOT, 'volumes/nginx')

conf = V.VMConfig()
conf.name = 'Cunik_by_VM'
conf.kernel_path = os.path.join(images_root, 'kernel.bin')
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
conf.vdisk_path = os.path.join(volumes_root, 'rootfs.iso')
conf.nic_name = 'tap0'
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
