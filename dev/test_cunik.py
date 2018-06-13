import os
import sys
sys.path.append(os.path.abspath('.'))

from api.models import Cunik, CunikConfig

import config

image_root = os.path.join(config.cunik_root, 'images/nginx')

cfg = CunikConfig(
    name='cunik0',
    img=os.path.join(image_root, 'kernel.img'),
    cmd=CunikConfig.fill(os.path.join(image_root, 'cmdline'), os.path.join(image_root, 'params.json')),
    vmm='kvm',
    mem='409600',
    data_volume=os.path.join(image_root, 'rootfs.iso'),
)

cu = Cunik(cfg)
input('waiting')
cu.start()
input('started')
cu.stop()
input('stopped')
