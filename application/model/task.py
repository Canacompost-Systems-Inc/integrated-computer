from dataclasses import dataclass
from typing import Optional

from application.model.routine.routine import Routine
from application.model.state.isolation.isolation_state import IsolationState


@dataclass
class Task:
    """Class for performing a routine in a particular isolation state"""
    routine: Routine
    isolation_state: Optional[IsolationState] = None
