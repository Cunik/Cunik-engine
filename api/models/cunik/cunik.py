"""class Cunik."""


class CunikConfig:
    """Config of a Cunik, constructed when the user wants to create a Cunik."""
    def __init__(self):
        pass


class Cunik:
    """Represent an existing Cunik."""
    @staticmethod
    def create(config: CunikConfig):
        """Create a Cunik according to the config."""
        # Deal with the config using unikernel backends
        # Create virtual machine using vm backends
        # Register in the Cunik registry
        pass

    @staticmethod
    def destroy(cunik: Cunik):
        """Destroy a Cunik according to the config."""
        # Stop the vm
        # Delete it from Cunik registry.
        pass

    def __init__(self):
        """Take configuration and create a Cunik(vm with unikernel)."""
        pass

    def start(self):
        """Start the Cunik."""
        pass

    def stop(self):
        """Stop the Cunik."""
        pass
