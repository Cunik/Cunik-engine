"""class Cunik."""

from api.models.image import ImageRegistry
from backend.vm import VM


class CunikConfig:
    """Config of a cunik, constructed when the user wants to create a Cunik."""
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.image = kwargs['image']
        self.cmd = kwargs['cmd']


class Cunik:
    """Represent a cunik.

    All the public methods of this class will immediately
    affect cunik registry and virtual machine unless it raises an exception.

    Usage:
        >>> cu = Cunik(...)  # Now there is a new cunik in cunik registry along with the vm instance
        >>> cu.start()  # Now it starts, and the new status is updated in cunik registry
        >>> cu.stop()
        >>> del cu  # NOTICE: This really destroys corresponding vm and remove this cunik from registry
    """
    def __init__(self, config: CunikConfig):
        # Create the vm with the image
        self.vm = VM(config)
        # Register the cunik in the registry

    def start(self):
        """Start the cunik."""
        # Start the vm
        self.vm.start()
        # Update in registry

    def stop(self):
        """Stop the cunik."""
        # Stop the vm
        self.vm.stop()
        # Update in registry

    def __del__(self):
        """Destroy a cunik according to the config."""
        # Destroy the vm
        self.vm.destroy()
        # Remove from registry
