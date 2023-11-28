from flask import Flask
from handlers import Handlers
from config import MasterConfig
from functools import partial


class MasterServer:
    def __init__(self, config: MasterConfig):
        self.config = config
        self.logger = config.logger
        self.data_store = {}
        self.handlers = Handlers(self.data_store)
        self.app = None

    def setup(self):
        app = Flask(__name__)

        app.add_url_rule("/api/store", view_func=self.handlers.add_key, methods=["PUT"])
        app.add_url_rule(
            "/api/retrieve", view_func=self.handlers.get_key, methods=["GET"]
        )

        self.app = app

    def run(self):
        if self.app is None:
            self.setup()
        self.logger.info(f"Server is running on port {self.config.port}")
        self.app.run(debug=self.config.debug, port=self.config.port)
