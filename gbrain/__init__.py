"""Gbrain - Go-based brain/chat bot framework."""

from .core import BrainManager, Conversation, Message
from .cli import main

__version__ = "0.1.0"
__author__ = "peterwang619-ui"

__all__ = ["BrainManager", "Conversation", "Message", "main"]
