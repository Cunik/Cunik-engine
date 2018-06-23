import os
import sys
import time

sys.path.append(os.path.abspath('.'))

from api.models.cunik import CunikApi

L = [1, 2, 3, 4]

if 1 in L:
    CunikApi.create('redis-server', params={'ipv4_addr': '10.0.120.101'})
    CunikApi.create('redis-server', params={'ipv4_addr': '10.0.121.101'})
    print('created')
    time.sleep(2)

if 2 in L:
    os.system('redis-benchmark --csv -h 10.0.120.101 -c 50 -n 10000 -P 16')
    os.system('redis-benchmark --csv -h 10.0.121.101 -c 50 -n 10000 -P 16')

if 3 in L:
    for i in CunikApi.list():
        CunikApi.stop(i.id)
    print('stopped')

if 4 in L:
    for i in CunikApi.list():
        CunikApi.remove(i.id)
    print('removed')
