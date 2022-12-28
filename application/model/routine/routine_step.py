from dataclasses import dataclass
from typing import Optional

from application.model.action.action_set import ActionSet


@dataclass
class RoutineStep:
    """Class for performing a set of actions then waiting a certain number of seconds."""
    action_set: Optional[ActionSet] = None  # List of Actions to perform; if None, this is effectively a sleep
    duration_sec: int = 0  # Time to wait after performing this action
