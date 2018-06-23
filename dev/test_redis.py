import os
import sys
import time

sys.path.append(os.path.abspath('.'))

from api.models.cunik import CunikApi

CunikApi.create('redis-server', params={'ipv4_addr': '10.0.120.101'})
print('created')
time.sleep(2)
os.system('redis-benchmark --csv -h 10.0.120.101 -c 50 -n 10000 -P 16')
for i in CunikApi.list():
    CunikApi.stop(i.id)
print('stopped')
for i in CunikApi.list():
    CunikApi.remove(i.id)
print('removed')
