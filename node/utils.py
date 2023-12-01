import socket
import requests


def is_valid_ip(ip: str):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


def request_node_vote(
    node_ip: str, term: int, candidate_id: int, last_log_index: int
) -> bool:
    url = f"http://{node_ip}/api/request_vote"

    payload = {
        "candidate_id": candidate_id,
        "term": term,
        "last_log_index": last_log_index,
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": f"Received status code {response.status_code}",
                "message": {response.json()},
            }
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def run_election(
    node_ips: list[str], term: int, candidate_id: int, last_log_index: int
) -> bool:
    """performs the election process and returns True if win"""
    num_votes = 1 # person who starts election votes for himself
    for node_ip in node_ips:
        response = request_node_vote(node_ip, term, candidate_id, last_log_index)
        if response.get("voteGranted", True):
            num_votes += 1 
    
    num_voters = len(node_ips) + 1
    return num_votes, num_voters

def is_election_winner(num_voters: int, num_votes: int) -> bool:
    """returns true if you won a majority in the election"""
    return num_votes > num_voters // 2
