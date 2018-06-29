"""Implements interface for Rumprun unikernels."""


from backend.vm import VMConfig


# Takes Unikernel specific configs, generate a VMConfig
def preprocess(cmdline, system_volume):
    vmc = VMConfig()
    vmc.cmdline = cmdline
    return vmc
