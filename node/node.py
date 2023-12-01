from flask import Flask
from handlers import Handlers
from config import NodeConfig
from threading import Thread, Timer, Lock
import time
import random
from enum import Enum
from utils import run_election, is_election_winner


class RaftState(Enum):
    FOLLOWER = 1
    CANDIDATE = 2
    LEADER = 3


class Node:
    def __init__(self, config: NodeConfig):
        self.config = config
        self.logger = config.logger
        self.raft_nodes = []

        self.state = RaftState.FOLLOWER
        self.current_term = 0
        self.voted_for = None
        self.election_timer = None
        self.leader_id = None
        self.votes = 0

        self.handlers = Handlers(self.raft_nodes, self.current_term, self.voted_for, self.reset_election_timer)
        self.app = None
        self.lock = Lock()

    def reset_election_timer(self):
        self.logger.debug(f"Reseting election timer")
        if self.election_timer:
            self.election_timer.cancel()

        # Random timeout between 150ms to 300ms
        timeout = random.uniform(0.5, 1)
        self.election_timer = Timer(timeout, self.start_election)
        self.election_timer.start()

    def start_election(self):
        with Lock():
            self.current_term += 1
            self.logger.debug(f"Starting election for term {self.current_term}")
            self.state = RaftState.CANDIDATE
            self.voted_for = self.config.node_id

            num_votes, num_voters = run_election(
                raft_nodes, self.current_term, self.candidate_id, last_log_index=2
            )

            if is_election_winner(num_voters=num_voters, num_votes=num_votes):
                self.state = RaftState.LEADER
                self.leader_id = self.config.node_id
                self.logger.debug(
                    f"Won election for term {self.current_term} with {num_votes} votes out of {num_voters}"
                )
            else:
                self.logger.debug(f"Lost election for term {self.current_term}")
                self.state = RaftState.FOLLOWER
                self.leader_id = None

            self.reset_election_timer()

    def setup_remote_server(self):
        app = Flask(__name__)

        app.add_url_rule(
            "/api/add_raft_node",
            view_func=self.handlers.add_raft_node,
            methods=["POST"],
        )
        app.add_url_rule(
            "/api/request_vote", view_func=self.handlers.request_vote, methods=["POST"]
        )
        app.add_url_rul(
            "/api/append_entry", view_func=self.handlers.append_entry, methods=["POST"]
        )
        self.app = app

    def run_remote_server(self):
        if self.app is None:
            self.setup_remote_server()
        self.logger.info(f"Node Server is running on port {self.config.port}")
        self.app.run(debug=self.config.debug, port=self.config.port)

    def run(self):
        self.reset_election_timer()
        self.run_remote_server()
