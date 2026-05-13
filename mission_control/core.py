"""Core task management classes."""

from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any


class TaskStatus(Enum):
    """Task status enumeration."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Task:
    """Represents a single task."""
    id: str
    name: str
    status: TaskStatus = TaskStatus.PENDING
    description: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status.value,
            "description": self.description,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "result": self.result,
            "error": self.error,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        """Create task from dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            status=TaskStatus(data.get("status", "pending")),
            description=data.get("description", ""),
            created_at=data.get("created_at"),
            started_at=data.get("started_at"),
            completed_at=data.get("completed_at"),
            result=data.get("result"),
            error=data.get("error"),
            metadata=data.get("metadata", {}),
        )


class TaskManager:
    """Manages tasks and their lifecycle."""

    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = storage_path or str(
            __import__("pathlib").Path.home() / ".mission_control" / "tasks.json"
        )
        self._tasks: Dict[str, Task] = {}
        self._load()

    def _load(self):
        """Load tasks from storage."""
        try:
            import json
            from pathlib import Path

            path = Path(self.storage_path)
            if path.exists():
                with open(path, "r") as f:
                    data = json.load(f)
                    for task_data in data.values():
                        task = Task.from_dict(task_data)
                        self._tasks[task.id] = task
        except Exception:
            self._tasks = {}

    def _save(self):
        """Save tasks to storage."""
        try:
            import json
            from pathlib import Path

            path = Path(self.storage_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            data = {tid: task.to_dict() for tid, task in self._tasks.items()}
            with open(path, "w") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def create_task(self, name: str, description: str = "", **metadata) -> Task:
        """Create a new task."""
        import uuid

        task_id = str(uuid.uuid4())[:8]
        task = Task(
            id=task_id,
            name=name,
            description=description,
            metadata=metadata,
        )
        self._tasks[task_id] = task
        self._save()
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        return self._tasks.get(task_id)

    def list_tasks(self, status: Optional[TaskStatus] = None) -> List[Task]:
        """List all tasks, optionally filtered by status."""
        tasks = list(self._tasks.values())
        if status:
            tasks = [t for t in tasks if t.status == status]
        return sorted(tasks, key=lambda t: t.created_at, reverse=True)

    def update_task_status(
        self, task_id: str, status: TaskStatus, error: Optional[str] = None
    ) -> bool:
        """Update a task's status."""
        task = self._tasks.get(task_id)
        if not task:
            return False

        task.status = status
        if status == TaskStatus.RUNNING and not task.started_at:
            task.started_at = datetime.now().isoformat()
        if status in (TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED):
            task.completed_at = datetime.now().isoformat()
        if error:
            task.error = error
        self._save()
        return True

    def complete_task(self, task_id: str, result: Optional[Dict] = None) -> bool:
        """Mark a task as completed."""
        task = self._tasks.get(task_id)
        if not task:
            return False
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.now().isoformat()
        if result:
            task.result = result
        self._save()
        return True

    def delete_task(self, task_id: str) -> bool:
        """Delete a task."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            self._save()
            return True
        return False
