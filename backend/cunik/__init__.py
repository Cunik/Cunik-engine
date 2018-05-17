"""Implementation of interfaces like create."""

import backend.vm as vm


class Config:
    pass


def create(conf: Config):
    """Create a Cunik specified by image_name.
        Get image path, then pass image path and command line to the vm.
    """
    vmconf = vm.Config()
    # ...
    vm.create(vmconf)
