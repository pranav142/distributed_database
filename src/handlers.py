from flask import jsonify, request


class Handlers:
    def __init__(self, data_store: dict):
        self.data_store = data_store

    def add_key(self):
        key = request.json.get("key")
        value = request.json.get("value")

        if key in self.data_store:
            return jsonify({"error": "Key already exists. Data not stored."}), 409

        if key is None or value is None:
            return jsonify({"error": "Key and value are required."}), 400

        self.data_store[key] = value
        return jsonify({"message": "Data stored successfully."}), 201

    def get_key(self):
        key = request.args.get("key")

        if key is None:
            return jsonify({"error": "Key is required."}), 400

        if key not in self.data_store:
            return jsonify({"error": "Data not found."}), 404

        value = self.data_store[key]
        return jsonify({"key": key, "value": value}), 200
