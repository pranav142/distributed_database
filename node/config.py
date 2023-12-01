import yaml
from dataclasses import dataclass, field
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

@dataclass
class NodeConfig:
    port: int = field(default=5000)
    debug: bool = field(default=True)
    name: str = field(default="Node")  
    logger: logging.Logger = field(
        default=logging.getLogger("Node"), repr=False, compare=False
    )
    node_id: int = field(default=None)

    def __post_init__(self):
        if self.debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

def load_config_from_yaml(file_path: str) -> NodeConfig:
    with open(file_path, "r") as file:
        config_data = yaml.safe_load(file)
    config = NodeConfig(**config_data)
    config.logger.info(f"Configuration loaded from {file_path}")
    return config
