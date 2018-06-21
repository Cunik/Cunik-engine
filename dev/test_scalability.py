import os
import sys
import time

sys.path.append(os.path.abspath('.'))

from api.models.cunik import CunikApi

import config

image_root = os.path.join(config.cunik_root, 'images/nginx')

T = 200

delay_time = 2

start_time = time.time()

for i in range(1, T + 1):
    CunikApi.create('nginx', params={'ipv4_addr': '10.{}.{}.101'.format(120 + i // 100, 120 + i % 100)})
    print('Started cunik{}'.format(i))

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

for i in CunikApi.list():
    CunikApi.stop(i.id)

print('All stopped')

for i in CunikApi.list():
    CunikApi.remove(i.id)

print('All removed')
