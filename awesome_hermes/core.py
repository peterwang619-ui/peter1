"""Core skill catalog classes."""

import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class SkillEntry:
    """Represents a skill in the catalog."""
    name: str
    description: str
    category: str = "other"
    installed: bool = False
    repo_url: str = ""
    installed_path: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "installed": self.installed,
            "repo_url": self.repo_url,
            "installed_path": self.installed_path,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SkillEntry":
        """Create from dictionary."""
        return cls(
            name=data["name"],
            description=data.get("description", ""),
            category=data.get("category", "other"),
            installed=data.get("installed", False),
            repo_url=data.get("repo_url", ""),
            installed_path=data.get("installed_path", ""),
        )


class SkillCatalog:
    """Manages the skill catalog."""

    # Default skills to populate the catalog
    DEFAULT_SKILLS = [
        SkillEntry("repomix", "Pack repository into single file", "dev-tools", False, "https://github.com/yamadashy/repomix"),
        SkillEntry("stack", "Go project stack management", "dev-tools", True, "", "/tmp/peter1/stack"),
        SkillEntry("gstack", "Golang stack tool", "dev-tools", False, "https://github.com/peterwang619-ui/peter1"),
        SkillEntry("mission-control", "Task orchestration and scheduling", "task-management", True, "", "/tmp/peter1/mission_control"),
        SkillEntry("hermes-workspace", "Multi-project workspace manager", "task-management", True, "", "/tmp/peter1/hermes_workspace"),
        SkillEntry("tokscale", "Token counting and estimation", "analysis", True, "", "/tmp/peter1/tokscale"),
        SkillEntry("hindsight", "Session search and memory management", "analysis", True, "", "/tmp/peter1/hindsight"),
        SkillEntry("awesome-hermes", "Curated collection of Hermes skills", "meta", True, "", "/tmp/peter1/awesome_hermes"),
    ]

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = Path(config_path or Path.home() / ".hermes" / "awesome-hermes.json")
        self.skills: Dict[str, SkillEntry] = {}
        self._load()
        if not self.skills:
            self._init_defaults()

    def _init_defaults(self):
        """Initialize with default skills."""
        for skill in self.DEFAULT_SKILLS:
            self.skills[skill.name] = skill
        self._save()

    def _load(self):
        """Load skill catalog."""
        try:
            if self.config_path.exists():
                with open(self.config_path, "r") as f:
                    data = json.load(f)
                    for name, skill_data in data.get("skills", {}).items():
                        self.skills[name] = SkillEntry.from_dict(skill_data)
        except Exception:
            self.skills = {}

    def _save(self):
        """Save skill catalog."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "skills": {name: skill.to_dict() for name, skill in self.skills.items()},
            }
            with open(self.config_path, "w") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def list_all(self) -> List[SkillEntry]:
        """List all skills in catalog."""
        return list(self.skills.values())

    def get_skill(self, name: str) -> Optional[SkillEntry]:
        """Get a skill by name."""
        return self.skills.get(name)

    def search(self, query: str) -> List[SkillEntry]:
        """Search skills by keyword."""
        query_lower = query.lower()
        results = []
        for skill in self.skills.values():
            if (query_lower in skill.name.lower() or
                query_lower in skill.description.lower() or
                query_lower in skill.category.lower()):
                results.append(skill)
        return results

    def recommend(self, description: str) -> List[SkillEntry]:
        """Recommend skills based on a task description."""
        description_lower = description.lower()
        recommendations = []

        # Simple keyword-based recommendation
        keywords = {
            "token": ["tokscale"],
            "count": ["tokscale"],
            "memory": ["hindsight"],
            "session": ["hindsight"],
            "task": ["mission-control"],
            "schedule": ["mission-control"],
            "project": ["hermes-workspace"],
            "workspace": ["hermes-workspace"],
            "go": ["stack", "gstack"],
            "golang": ["stack", "gstack"],
            "build": ["stack"],
            "repo": ["repomix"],
            "pack": ["repomix"],
        }

        for keyword, skill_names in keywords.items():
            if keyword in description_lower:
                for skill_name in skill_names:
                    skill = self.skills.get(skill_name)
                    if skill and skill not in recommendations:
                        recommendations.append(skill)

        return recommendations

    def mark_installed(self, name: str, path: str = ""):
        """Mark a skill as installed."""
        if name in self.skills:
            self.skills[name].installed = True
            if path:
                self.skills[name].installed_path = path
            self._save()

    def add_skill(self, skill: SkillEntry):
        """Add a new skill to the catalog."""
        self.skills[skill.name] = skill
        self._save()
