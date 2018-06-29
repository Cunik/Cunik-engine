import os
import sys
import time

sys.path.append(os.path.abspath('.'))

from api.models.cunik import CunikApi

from api.config import default_config

image_root = os.path.join(default_config.CUNIK_ROOT, 'images/nginx')

T = 200

delay_time = 2

start_time = time.time()

for i in range(1, T + 1):
    CunikApi.create('nginx', params={'ipv4_addr': '10.120.{}.101'.format(i)})
    print('Started cunik{}'.format(i))
cnt = 0

end_time = time.time()

print('Time elapsed: {} sec'.format(end_time - start_time - delay_time))

input('All running')

for i in CunikApi.list():
    CunikApi.stop(i.uuid)

print('All stopped')

for i in CunikApi.list():
    CunikApi.remove(i.uuid)

print('All removed')
