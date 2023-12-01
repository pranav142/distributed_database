import pytest
from node.raft_log import RaftFileLog, LogEntry, serialize_file_log_entry, deserialize_file_log_entry

def test_log_entry():
    valid_command = "PUT weHave bigSwag"

    # Invalid command
    with pytest.raises(ValueError):
        invalid_entry = LogEntry(leader_commit_index=10, index=1, term=20, command="INVALID not valid")

    # Invalid leader_commit_index
    with pytest.raises(ValueError):
        invalid_entry = LogEntry(leader_commit_index=-1, index=1, term=20, command=valid_command)
    
    # Invalid Index
    with pytest.raises(ValueError):
        invalid_entry = LogEntry(leader_commit_index=10, index=-1, term=20, command=valid_command)

    # Invalid Term
    with pytest.raises(ValueError):
        invalid_entry = LogEntry(leader_commit_index=10, index=1, term=-20, command=valid_command)

def test_serialize_file_log_entry():
    entry = LogEntry(leader_commit_index=10, index=1, term=20, command="PUT weHave bigSwag")
    serialzed_entry = serialize_file_log_entry(entry)

    assert serialzed_entry == "1,20,10,PUT weHave bigSwag"

    entry = LogEntry(leader_commit_index=10, index=1, term=20, command="GET weHave")
    serialzed_entry = serialize_file_log_entry(entry)

    assert serialzed_entry == "1,20,10,GET weHave"
def test_deserialize_file_log_entry(): 
    serialized_entry = "1,20,10,PUT weHave bigSwag"
    log_entry = deserialize_file_log_entry(serialized_entry)

    assert log_entry.index == 1
    assert log_entry.term == 20
    assert log_entry.leader_commit_index == 10
    assert log_entry.command == "PUT weHave bigSwag" 