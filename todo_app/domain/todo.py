from dataclasses import dataclass
from typing import Optional

@dataclass
class Todo:
    """Represents a single task in the system."""
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed
        }
