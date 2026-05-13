"""Cross-session memory management."""

import json
from pathlib import Path
from typing import Dict, Optional


def _get_memory_file() -> Path:
    """Get the memory file path."""
    return Path.home() / ".hindsight" / "memory.json"


def load_memory(key: Optional[str] = None):
    """
    Load memory entries.

    Args:
        key: Specific key to load. If None, returns all memory.

    Returns:
        Memory value(s).
    """
    memory_file = _get_memory_file()
    if not memory_file.exists():
        return {} if key is None else None

    try:
        with open(memory_file, "r") as f:
            data = json.load(f)
        return data if key is None else data.get(key)
    except (json.JSONDecodeError, IOError):
        return {} if key is None else None


def save_memory(key: str, value) -> bool:
    """
    Save a memory entry.

    Args:
        key: Memory key.
        value: Value to store (must be JSON-serializable).

    Returns:
        True if successful.
    """
    memory_file = _get_memory_file()
    memory_file.parent.mkdir(parents=True, exist_ok=True)

    data = {}
    if memory_file.exists():
        try:
            with open(memory_file, "r") as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            data = {}

    data[key] = value

    try:
        with open(memory_file, "w") as f:
            json.dump(data, f, indent=2)
        return True
    except IOError:
        return False


def delete_memory(key: str) -> bool:
    """
    Delete a memory entry.

    Args:
        key: Memory key to delete.

    Returns:
        True if successful.
    """
    memory_file = _get_memory_file()
    if not memory_file.exists():
        return False

    try:
        with open(memory_file, "r") as f:
            data = json.load(f)
        if key in data:
            del data[key]
            with open(memory_file, "w") as f:
                json.dump(data, f, indent=2)
            return True
    except (json.JSONDecodeError, IOError):
        pass

    return False
