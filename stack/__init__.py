"""Stack - Go project stack management tool."""

from .core import StackManager, GoProject
from .cli import main

__version__ = "0.1.0"
__author__ = "peterwang619-ui"

__all__ = ["StackManager", "GoProject", "main"]
