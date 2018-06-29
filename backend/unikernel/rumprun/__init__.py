"""Implements interface for Rumprun unikernels."""


from backend.vm import VMConfig


# Takes Unikernel specific configs, generate a VMConfig
def preprocess(image_root, cmdline):
    return cmdline
