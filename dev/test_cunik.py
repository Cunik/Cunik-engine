import os
import sys
import time

sys.path.append(os.path.abspath('.'))

from api.models import Cunik, CunikConfig

os.system('ip l del tap0 2>/dev/null')
os.system('ip tuntap add tap0 mode tap')
os.system('ip addr add 10.0.120.100/24 dev tap0')
os.system('ip link set dev tap0 up')

cfg = CunikConfig(
    name='cunik0',
    image='nginx0.0.1',
    cmdline=CunikConfig.fill('images/nginx/cmdline', 'images/nginx/params.json'),
    hypervisor='kvm',
    memory='40960',
    data_volume='nginx_test_volume',
    nic='tap0'
)

cu = Cunik(cfg)
print('waiting')
cu.start()
print('started')
time.sleep(2)
os.system('curl 10.0.120.101')
cu.stop()
print('stopped')
