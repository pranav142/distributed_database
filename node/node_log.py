from typing import Protocol
from dataclasses import dataclass, field


@dataclass
class LogEntry:
    leader_commit_index: int
    index: int
    term: int
    command: str


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
    pass


def deserialize_file_log_entry(serialized_entry: str) -> LogEntry:
    pass
