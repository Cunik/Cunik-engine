import json

tmp = {
    'ipv4_addr': '10.0.120.101',
    'extra_cmdline': './nginx.bin -c /data/conf/nginx.conf'
}

print(json.dumps(tmp, indent=4, sort_keys=False))
