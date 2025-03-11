import os
import importlib.util
from modules.base_plugin import BasePlugin

def load_plugins():
    """Dynamically loads all plugins in the 'modules' directory."""
    plugins = {}

    module_path = os.path.join(os.path.dirname(__file__), "..", "modules")
    
    for filename in os.listdir(module_path):
        if filename.endswith(".py") and filename != "base_plugin.py":
            module_name = filename[:-3]
            module_spec = importlib.util.spec_from_file_location(module_name, f"{module_path}/{filename}")
            module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module)

            for attr in dir(module):
                cls = getattr(module, attr)
                if isinstance(cls, type) and issubclass(cls, BasePlugin) and cls is not BasePlugin:
                    plugin_instance = cls()
                    plugins[plugin_instance.name] = plugin_instance

    return plugins
