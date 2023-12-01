import argparse
from config import load_config_from_yaml
from node import Node

def main():
    parser = argparse.ArgumentParser(description="Run the server node.")
    parser.add_argument("-c", "--config", required=True, help="Path to the configuration YAML file.")
    
    args = parser.parse_args()
    config_path = args.config

    config = load_config_from_yaml(config_path)
    server = Node(config)

    server.run()

if __name__ == "__main__":
    main()
