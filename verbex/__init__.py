import importlib.metadata

from .verbex import CharClass as CharClass
from .verbex import SpecialChar as SpecialChar
from .verbex import Verbex as Verbex

__version__ = importlib.metadata.version("verbex")
