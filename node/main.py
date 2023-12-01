from config import load_config_from_yaml
from node import Node

CONFIG_PATH = "../configs/node1_config.yaml"


def main():
    config = load_config_from_yaml(CONFIG_PATH)
    server = Node(config)

    server.run()


if __name__ == "__main__":
    main()
