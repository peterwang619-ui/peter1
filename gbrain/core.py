"""Core brain/chat bot classes."""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class Message:
    """Represents a single message in a conversation."""
    role: str  # "user" or "assistant"
    content: str
    timestamp: str = ""

    def to_dict(self) -> dict:
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Message":
        return cls(
            role=data["role"],
            content=data["content"],
            timestamp=data.get("timestamp", ""),
        )


@dataclass
class Conversation:
    """Represents a conversation session."""
    id: str
    title: str
    messages: List[Message] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "messages": [m.to_dict() for m in self.messages],
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Conversation":
        messages = [Message.from_dict(m) for m in data.get("messages", [])]
        return cls(
            id=data["id"],
            title=data.get("title", "Untitled"),
            messages=messages,
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
        )

    def add_message(self, role: str, content: str):
        """Add a message to the conversation."""
        msg = Message(
            role=role,
            content=content,
            timestamp=datetime.now().isoformat(),
        )
        self.messages.append(msg)
        self.updated_at = datetime.now().isoformat()

    def get_history(self, limit: int = 10) -> List[Message]:
        """Get recent message history."""
        return self.messages[-limit:] if limit else self.messages


class BrainManager:
    """Manages brain/chat bot conversations."""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = Path(config_path or Path.home() / ".hermes" / "gbrain.json")
        self.conversations: Dict[str, Conversation] = {}
        self.current_conversation: Optional[str] = None
        self._load()

    def _load(self):
        """Load conversations from storage."""
        try:
            if self.config_path.exists():
                with open(self.config_path, "r") as f:
                    data = json.load(f)
                    for conv_data in data.get("conversations", []):
                        conv = Conversation.from_dict(conv_data)
                        self.conversations[conv.id] = conv
                    self.current_conversation = data.get("current")
        except Exception:
            self.conversations = {}

    def _save(self):
        """Save conversations to storage."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "conversations": [c.to_dict() for c in self.conversations.values()],
                "current": self.current_conversation,
            }
            with open(self.config_path, "w") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def create_conversation(self, title: str = "") -> Conversation:
        """Create a new conversation."""
        import uuid

        conv_id = str(uuid.uuid4())[:8]
        from datetime import datetime

        conv = Conversation(
            id=conv_id,
            title=title or f"Conversation {conv_id}",
            created_at=datetime.now().isoformat(),
        )
        self.conversations[conv_id] = conv
        if not self.current_conversation:
            self.current_conversation = conv_id
        self._save()
        return conv

    def get_conversation(self, conv_id: str) -> Optional[Conversation]:
        """Get a conversation by ID."""
        return self.conversations.get(conv_id)

    def list_conversations(self) -> List[Conversation]:
        """List all conversations."""
        return sorted(
            self.conversations.values(),
            key=lambda c: c.updated_at or c.created_at,
            reverse=True,
        )

    def delete_conversation(self, conv_id: str) -> bool:
        """Delete a conversation."""
        if conv_id in self.conversations:
            del self.conversations[conv_id]
            if self.current_conversation == conv_id:
                self.current_conversation = None
            self._save()
            return True
        return False

    def send_message(self, conv_id: str, content: str) -> Optional[Message]:
        """Send a user message to a conversation."""
        conv = self.conversations.get(conv_id)
        if not conv:
            return None
        conv.add_message("user", content)
        self._save()
        return conv.messages[-1]

    def reply(self, conv_id: str, content: str) -> Optional[Message]:
        """Add an assistant reply to a conversation."""
        conv = self.conversations.get(conv_id)
        if not conv:
            return None
        conv.add_message("assistant", content)
        self._save()
        return conv.messages[-1]

    def switch_conversation(self, conv_id: str) -> bool:
        """Switch to a different conversation."""
        if conv_id in self.conversations:
            self.current_conversation = conv_id
            self._save()
            return True
        return False

    def get_current_conversation(self) -> Optional[Conversation]:
        """Get the currently active conversation."""
        if self.current_conversation:
            return self.conversations.get(self.current_conversation)
        return None
