#!/bin/bash

ip l del tap0 2>/dev/null

ip tuntap add tap0 mode tap                                     
ip addr add 10.0.120.100/24 dev tap0
ip link set dev tap0 up

python3 dev/test_vm.py
