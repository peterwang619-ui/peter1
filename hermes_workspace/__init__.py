"""Hermes Workspace - Multi-project workspace manager."""

from .core import WorkspaceManager, Project
from .cli import main

__version__ = "0.1.0"
__author__ = "peterwang619-ui"

__all__ = ["WorkspaceManager", "Project", "main"]
