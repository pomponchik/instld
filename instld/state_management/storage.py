from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Optional


class RunType(IntEnum):
    script = auto()
    REPL = auto()
    module = auto()

@dataclass
class StateStorage:
    run_type: RunType = RunType.module
    last_string: Optional[str] = None


state_storage = StateStorage()
