import json

tmp = {
    'name': 'Cunik0',
    'img': 'test_kernel',
    'cmd': 'test_cmdline',
    'par': '',
    'vmm': 'kvm',
    'mem': '409600',
    'data_volume': 'test_volume',
    'data_volume_mount_point': '/data',
}

print(json.dumps(tmp, indent=4, sort_keys=False))
