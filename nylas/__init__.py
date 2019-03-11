from pkgutil import extend_path
from .client.client import APIClient

# Allow out-of-tree submodules.
__path__ = extend_path(__path__, __name__)
__all__ = ["APIClient"]
