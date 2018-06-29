import os
import sys
import time

sys.path.append(os.path.abspath('.'))

from api.models.cunik import CunikApi

CunikApi.create('nginx', params={'ipv4_addr': '10.0.120.101'})
print('created')
time.sleep(2)
print('waiting')
os.system('curl 10.0.120.101')
for i in CunikApi.list():
    CunikApi.stop(i.uuid)
print('stopped')
for i in CunikApi.list():
    CunikApi.remove(i.uuid)
print('removed')
