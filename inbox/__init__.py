from pkgutil import extend_path

# Allow out-of-tree submodules.
__path__ = extend_path(__path__, __name__)
