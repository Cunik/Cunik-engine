import os
import sys
import time

sys.path.append(os.path.abspath('.'))

from api.models.cunik import CunikApi

L = [1, 2, 3, 4]

ip_addr1 = '10.0.220.101'
ip_addr2 = '10.0.221.101'

if 1 in L:
    CunikApi.create('redis-server', params={'ipv4_addr': ip_addr1})
    CunikApi.create('redis-server', params={'ipv4_addr': ip_addr2})
    print('created')
    time.sleep(2)

if 2 in L:
    os.system('redis-benchmark --csv -h {} -c 50 -n 1000 -P 16'.format(ip_addr1))
    os.system('redis-benchmark --csv -h {} -c 50 -n 1000 -P 16'.format(ip_addr2))

if 3 in L:
    for i in CunikApi.list():
        CunikApi.stop(i.uuid)
    print('stopped')

if 4 in L:
    for i in CunikApi.list():
        CunikApi.remove(i.uuid)
    print('removed')
