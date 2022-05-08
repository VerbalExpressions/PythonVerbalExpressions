try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version  # type: ignore

from .verbex import CharClass as CharClass
from .verbex import SpecialChar as SpecialChar
from .verbex import Verbex as Verbex

__version__ = version("verbex")
