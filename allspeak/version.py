import pkg_resources


try:
    __version__ = pkg_resources.require("allspeak")[0].version
except Exception:  # pragma:no cover
    # Run pytest without needing to install the library
    __version__ = None
