from flask import jsonify, request
from utils import is_valid_ip
import logging


class Handlers:
    def __init__(
        self,
        logger: logging.Logger,
        peers: list[str],
        term: int,
        voted_for: int,
        reset_election_timer_cb: callable,
    ):
        self.logger = logger
        self.peers = peers
        self.current_term = term
        self.voted_for = voted_for
        self.reset_election_timer_cb = reset_election_timer_cb

    def add_raft_node(self):
        self.logger.debug("Adding raft node handler")
        raft_node_ip = request.json.get("ip")

        if raft_node_ip in self.peers:
            return jsonify({"error": "Raft node has already been added to node"}), 409

        if raft_node_ip is None:
            return jsonify({"error": "Raft node ip is required"}), 400

        # if not is_valid_ip(raft_node_ip):
        #     return jsonify({"error": "Invalid raft node ip"}), 400

        self.peers.append(raft_node_ip)
        return jsonify({"message": "Raft node added successfully"}), 201

    def request_vote(self):
        
        canidate_id = request.json.get("canidate_id")
        term = request.json.get("current_term")
        last_log_index = request.json.get("last_log_index")

        self.logger.debug(f"Request vote handler from Node_{canidate_id}")

        if term < self.current_term:
            return (
                jsonify({"voteGranted": False, "currentTerm": self.current_term}),
                409,
            )

        if self.voted_for is not None and self.voted_for != candidate_id:
            return (
                jsonify({"voteGranted": False, "currentTerm": self.current_term}),
                409,
            )

        self.voted_for = candidate_id
        self.current_term = term
        return jsonify({"voteGranted": True, "currentTerm": self.current_term}), 200

    def append_entry(self):
        
        leader_commit_index = request.json.get(
            "leader_commit_index"
        )  # Integer on whether to commit last append entry
        index = request.json.get("index")
        term = request.json.get("term")
        command = request.json.get("command")  # PUT key value, GET key

        self.logger.debug(f"Append Entry request")

        # put entry in the log if certain case is fulfilled
        self.reset_election_timer_cb()
