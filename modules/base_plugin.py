class BasePlugin:
    """Base class for all AWS toolkit plugins."""

    def __init__(self, name, category, description):
        self.name = name
        self.category = category  # New category field
        self.description = description

    def run(self, region=None):
        """Method to be overridden in each plugin."""
        raise NotImplementedError("Plugins must implement the 'run' method.")
