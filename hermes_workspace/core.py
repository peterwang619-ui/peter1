"""Core workspace management classes."""

import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class Project:
    """Represents a project in the workspace."""
    name: str
    path: str
    description: str = ""
    created_at: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "path": self.path,
            "description": self.description,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        """Create from dictionary."""
        return cls(
            name=data["name"],
            path=data["path"],
            description=data.get("description", ""),
            created_at=data.get("created_at", ""),
        )


class WorkspaceManager:
    """Manages multiple projects in a workspace."""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = Path(config_path or Path.home() / ".hermes" / "workspace.json")
        self.projects: Dict[str, Project] = {}
        self.current_project: Optional[str] = None
        self._load()

    def _load(self):
        """Load workspace configuration."""
        try:
            if self.config_path.exists():
                with open(self.config_path, "r") as f:
                    data = json.load(f)
                    for name, proj_data in data.get("projects", {}).items():
                        self.projects[name] = Project.from_dict(proj_data)
                    self.current_project = data.get("current")
        except Exception:
            self.projects = {}
            self.current_project = None

    def _save(self):
        """Save workspace configuration."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "projects": {name: proj.to_dict() for name, proj in self.projects.items()},
                "current": self.current_project,
            }
            with open(self.config_path, "w") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def add_project(self, name: str, path: str, description: str = "") -> Project:
        """Add a new project to the workspace."""
        from datetime import datetime
        project = Project(
            name=name,
            path=path,
            description=description,
            created_at=datetime.now().isoformat(),
        )
        self.projects[name] = project
        if not self.current_project:
            self.current_project = name
        self._save()
        return project

    def remove_project(self, name: str) -> bool:
        """Remove a project from the workspace."""
        if name in self.projects:
            del self.projects[name]
            if self.current_project == name:
                self.current_project = None
            self._save()
            return True
        return False

    def list_projects(self) -> List[Project]:
        """List all projects in the workspace."""
        return list(self.projects.values())

    def get_project(self, name: str) -> Optional[Project]:
        """Get a specific project by name."""
        return self.projects.get(name)

    def switch_project(self, name: str) -> bool:
        """Switch to a different project."""
        if name in self.projects:
            self.current_project = name
            self._save()
            return True
        return False

    def get_current_project(self) -> Optional[Project]:
        """Get the currently active project."""
        if self.current_project:
            return self.projects.get(self.current_project)
        return None
