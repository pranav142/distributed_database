from flask import jsonify, request
from utils import is_valid_ip


class Handlers:
    def __init__(self, raft_nodes: list[str]):
        self.raft_nodes = raft_nodes

    def add_raft_node(self):
        raft_node_ip = request.json.get("ip")

        if raft_node_ip in self.raft_nodes:
            return jsonify({"error": "Raft node has already been added to node"}), 409

        if raft_node_ip is None:
            return jsonify({"error": "Raft node ip is required"}), 400

        # if not is_valid_ip(raft_node_ip):
        #     return jsonify({"error": "Invalid raft node ip"}), 400

        self.raft_nodes.append(raft_node_ip)
        return jsonify({"message": "Raft node added successfully"}), 201
