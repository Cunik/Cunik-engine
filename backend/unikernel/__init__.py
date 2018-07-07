from .rumprun import Rumprun
from .osv import OSv


unikernels = {
    'rumprun': Rumprun,
    'osv': OSv,
}


def configure(image, config, nic_name):
    """Construct a vm config from cunik config using different Unikernel backends."""
    # TODO: We should have better way to do this
    return unikernels[image.unikernel].configure(image, config, nic_name)
