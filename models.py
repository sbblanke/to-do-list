from dataclasses import dataclass
from enum import Enum


class Workband(Enum):
    NOW = "Now"
    NEXT = "Next"
    LATER = "Later"
    BLOCKED = "Blocked"


@dataclass
class Task:
    number: int
    name: str
    description: str
    Workband: Workband
    completed: bool = False
