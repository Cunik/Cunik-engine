import json

tmp = {
    'namespace': 'core',
    'name': 'nginx',
    'version': '0.0.1',
    'description': 'Nginx Web server',
    'unikernel': {
        'name': 'rumpkernel',
        'version': None,
        'url': 'http://rumpkernel.org/',
    },
    'platforms': [
        'kvm'
    ]
}

print(json.dumps(tmp, indent=4, sort_keys=False))
