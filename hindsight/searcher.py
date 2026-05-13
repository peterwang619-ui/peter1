"""Session search and retrospective analysis."""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


def _get_sessions_dir() -> Path:
    """Get the sessions directory path."""
    return Path.home() / ".hindsight" / "sessions"


def list_sessions(limit: int = 10) -> List[Dict]:
    """
    List recent sessions.

    Args:
        limit: Maximum number of sessions to return.

    Returns:
        List of session info dicts.
    """
    sessions_dir = _get_sessions_dir()
    if not sessions_dir.exists():
        return []

    sessions = sorted(
        sessions_dir.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    result = []
    for session_file in sessions[:limit]:
        try:
            with open(session_file, "r") as f:
                data = json.load(f)
                result.append({
                    "id": session_file.stem,
                    "title": data.get("title", "Untitled"),
                    "timestamp": data.get("timestamp", ""),
                    "preview": data.get("content", "")[:100],
                })
        except (json.JSONDecodeError, IOError):
            continue

    return result


def search_sessions(query: str, limit: int = 10) -> List[Dict]:
    """
    Search sessions by keyword.

    Args:
        query: Search keyword.
        limit: Maximum number of results.

    Returns:
        List of matching session info dicts.
    """
    sessions_dir = _get_sessions_dir()
    if not sessions_dir.exists():
        return []

    query_lower = query.lower()
    results = []

    for session_file in sessions_dir.glob("*.json"):
        try:
            with open(session_file, "r") as f:
                data = json.load(f)
                content = data.get("content", "").lower()
                title = data.get("title", "").lower()

                if query_lower in content or query_lower in title:
                    results.append({
                        "id": session_file.stem,
                        "title": data.get("title", "Untitled"),
                        "timestamp": data.get("timestamp", ""),
                        "preview": data.get("content", "")[:100],
                    })
        except (json.JSONDecodeError, IOError):
            continue

    return results[:limit]


def save_session(session_id: str, title: str, content: str) -> bool:
    """
    Save a session to disk.

    Args:
        session_id: Unique session identifier.
        title: Session title.
        content: Session content.

    Returns:
        True if successful.
    """
    sessions_dir = _get_sessions_dir()
    sessions_dir.mkdir(parents=True, exist_ok=True)

    data = {
        "id": session_id,
        "title": title,
        "content": content,
        "timestamp": datetime.now().isoformat(),
    }

    try:
        with open(sessions_dir / f"{session_id}.json", "w") as f:
            json.dump(data, f, indent=2)
        return True
    except IOError:
        return False
