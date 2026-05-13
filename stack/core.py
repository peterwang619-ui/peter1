"""Core stack management classes for Go projects."""

import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class GoProject:
    """Represents a Go project."""
    name: str
    path: str
    module: str = ""
    created_at: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "path": self.path,
            "module": self.module,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "GoProject":
        """Create from dictionary."""
        return cls(
            name=data["name"],
            path=data["path"],
            module=data.get("module", ""),
            created_at=data.get("created_at", ""),
        )


class StackManager:
    """Manages Go project stacks."""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = Path(config_path or Path.home() / ".hermes" / "stack.json")
        self.projects: Dict[str, GoProject] = {}
        self._load()

    def _load(self):
        """Load stack configuration."""
        try:
            if self.config_path.exists():
                with open(self.config_path, "r") as f:
                    data = json.load(f)
                    for name, proj_data in data.get("projects", {}).items():
                        self.projects[name] = GoProject.from_dict(proj_data)
        except Exception:
            self.projects = {}

    def _save(self):
        """Save stack configuration."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "projects": {name: proj.to_dict() for name, proj in self.projects.items()},
            }
            with open(self.config_path, "w") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def init_project(self, name: str, path: str, module: str = "") -> GoProject:
        """Initialize a new Go project."""
        from datetime import datetime

        # If no module specified, use path-based module name
        if not module:
            module = f"github.com/{name}/{name}"

        project = GoProject(
            name=name,
            path=path,
            module=module,
            created_at=datetime.now().isoformat(),
        )

        # Create project directory and go.mod
        project_path = Path(path)
        project_path.mkdir(parents=True, exist_ok=True)

        try:
            subprocess.run(
                ["go", "mod", "init", module],
                cwd=str(project_path),
                capture_output=True,
                check=True,
            )
        except Exception:
            pass  # Ignore if go.mod already exists or go not installed

        self.projects[name] = project
        self._save()
        return project

    def list_projects(self) -> List[GoProject]:
        """List all Go projects."""
        return list(self.projects.values())

    def get_project(self, name: str) -> Optional[GoProject]:
        """Get a project by name."""
        return self.projects.get(name)

    def remove_project(self, name: str) -> bool:
        """Remove a project from stack."""
        if name in self.projects:
            del self.projects[name]
            self._save()
            return True
        return False

    def build_project(self, name: str) -> dict:
        """Build a Go project."""
        project = self.projects.get(name)
        if not project:
            return {"success": False, "error": "Project not found"}

        try:
            result = subprocess.run(
                ["go", "build", "-o", name, "."],
                cwd=project.path,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                return {"success": True, "output": result.stdout}
            else:
                return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def run_project(self, name: str, args: list = None) -> dict:
        """Run a Go project."""
        project = self.projects.get(name)
        if not project:
            return {"success": False, "error": "Project not found"}

        try:
            cmd = ["go", "run", "."]
            if args:
                cmd.extend(args)
            result = subprocess.run(
                cmd,
                cwd=project.path,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                return {"success": True, "output": result.stdout}
            else:
                return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}
