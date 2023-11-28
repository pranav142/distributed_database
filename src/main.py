from config import load_config_from_yaml
from server import MasterServer

CONFIG_PATH = "../configs/test_config.yaml"


def main():
    config = load_config_from_yaml(CONFIG_PATH)
    server = MasterServer(config)

    server.run()


if __name__ == "__main__":
    main()
