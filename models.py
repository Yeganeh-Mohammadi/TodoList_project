from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import uuid


@dataclass
class Task:
    title: str
    description: str = ""
    deadline: Optional[str] = None
    status: str = "todo"  # todo, doing, done
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def __str__(self):
        short_id = self.id[:8]  # show first 8 characters only
        task_titles = ", ".join([t.title for t in self.tasks]) or "no tasks"
        return f"📁 [{short_id}] {self.name} | Tasks: {task_titles}"


@dataclass
class Project:
    name: str
    description: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tasks: List[Task] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def __str__(self):
        short_id = self.id[:8]
        return f"[{self.status.upper()}] {self.title} (id={short_id}, deadline: {self.deadline or '—'})"
