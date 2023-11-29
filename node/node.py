from flask import Flask
from handlers import Handlers
from config import NodeConfig

class Node:
    def __init__(self, config: NodeConfig):
        self.config = config
        self.logger = config.logger
        self.raft_nodes = []
        self.handlers = Handlers(self.raft_nodes)
        self.app = None

    def setup(self):
        app = Flask(__name__)

        app.add_url_rule("/api/add_raft_node", view_func=self.handlers.add_raft_node, methods=["POST"])

        self.app = app

    def run(self):
        if self.app is None:
            self.setup()
        self.logger.info(f"Node Server is running on port {self.config.port}")
        self.app.run(debug=self.config.debug, port=self.config.port)
