import os
import sys
import time

sys.path.append(os.path.abspath('.'))

from api.models import Cunik, CunikConfig

import config

image_root = os.path.join(config.cunik_root, 'images/nginx')

T = 200

delay_time = 2

cu = [None] * T

start_time = time.time()

for i in range(1, T + 1):
    os.system('ip l del tap{} 2>/dev/null'.format(i))
    os.system('ip tuntap add tap{} mode tap'.format(i))
    os.system('ip addr add 10.{}.{}.100/24 dev tap{}'.format(120 + i // 100, 120 + i % 100, i))
    os.system('ip link set dev tap{} up'.format(i))
    cfg = CunikConfig(
        name='cunik{}'.format(i),
        image=os.path.join(image_root, 'kernel.img'),
        cmdline=CunikConfig.fill(os.path.join(image_root, 'cmdline'), os.path.join(image_root, 'params.json'),
                                 ipv4_addr="10.{}.{}.101".format(120 + i // 100, 120 + i % 100)),
        hypervisor='kvm',
        memory='40960',
        data_volume=os.path.join(image_root, 'rootfs.iso'),
        nic='tap{}'.format(i)
    )
    cu[i - 1] = Cunik(cfg)
    cu[i - 1].start()
    print('started cunik{}'.format(i))

time.sleep(delay_time)
cnt = 0

for i in range(1, T + 1):
    if not os.system('curl 10.{}.{}.101'.format(120 + i // 100, 120 + i % 100)):
        cnt += 1

end_time = time.time()

if cnt == T:
    print('TEST PASSED!')
else:
    print('TEST FAILED!')

print('Time elapsed: {} sec'.format(end_time - start_time - delay_time))

# input('')

for i in range(1, T + 1):
    cu[i - 1].stop()
