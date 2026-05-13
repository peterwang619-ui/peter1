"""TokScale - Token scaling and estimation tool for LLM context management."""

__version__ = "0.1.0"
__author__ = "peterwang619-ui"

from .counter import count_tokens, estimate_context

__all__ = ["count_tokens", "estimate_context"]
