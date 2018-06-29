"""Implements interface for OSv unikernels."""


from .imgedit import set_cmdline
from backend.vm import VMConfig
from sys import path


# Takes Unikernel specific configs, generate a VMConfig
def preprocess(image_root, cmdline):
    set_cmdline(path.join(image_root, 'system.qcow'), cmdline)
    return None
