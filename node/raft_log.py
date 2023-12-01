from typing import Protocol, Optional
from dataclasses import dataclass, field
from node.command import is_valid_command

@dataclass
class LogEntry:
    index: int
    term: int
    leader_commit_index: int
    command: Optional[str] = None

    def __post_init__(self):
        if self.leader_commit_index < 0:
            raise ValueError("leader_commit_index must be non-negative")
        if self.index < 0:
            raise ValueError("index must be non-negative")
        if self.term < 0:
            raise ValueError("term must be non-negative")
        if not is_valid_command(self.command):
            raise ValueError("Invalid command passed")

class RaftLog(Protocol):
    def append_entry(self, entry: LogEntry) -> None:
        ...

    def get_entry(self, index: int) -> LogEntry:
        ...

    def delete_entry(self, index: int) -> None:
        ...

    def get_last_entry(self) -> LogEntry:
        ...

    def get_current_log_term(self) -> int:
        ...

    def close(self) -> None:
        ...


class RaftFileLog(RaftLog):
    def __init__(self):
        pass

    def append_entry(self, entry: LogEntry) -> None:
        pass

    def delete_entry(self, index: int) -> LogEntry:
        pass

    def get_last_entry(self) -> LogEntry:
        pass

    def get_current_log_term(self) -> int:
        pass

    def close(self) -> None:
        pass


def serialize_file_log_entry(entry: LogEntry) -> str:
    return f"{entry.index},{entry.term},{entry.leader_commit_index},{entry.command}"

def deserialize_file_log_entry(serialized_entry: str) -> LogEntry:
    args = serialized_entry.split(",")
    
    index = int(args[0])
    term = int(args[1])
    leader_commit_index = int(args[2])
    command = args[3] 

    return LogEntry(index=index, term=term, leader_commit_index=leader_commit_index, command=command)
