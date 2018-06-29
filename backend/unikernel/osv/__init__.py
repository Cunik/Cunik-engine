"""Implements interface for OSv unikernels."""


from .imgedit import set_cmdline
from backend.vm import VMConfig


# Takes Unikernel specific configs, generate a VMConfig
def preprocess(cmdline, system_volume):
    set_cmdline(system_volume, cmdline)
    vmc = VMConfig()
    return vmc
