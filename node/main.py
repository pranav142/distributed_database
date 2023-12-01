from config import load_config_from_yaml
from node import Node
from threading import Thread

BASE_DIR = "../configs/"

def main():

    threads = []

    for i in range(1, 3):
        config_dir = f"{BASE_DIR}/node{i}_config.yaml"
        config = load_config_from_yaml(config_dir)
        node = Node(config)

        thread = Thread(target=node.run)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
