import yaml
from dataclasses import dataclass, field
import logging
from utils import get_default_logger

@dataclass
class MasterConfig:
    port: int = field(default=5000)
    debug: bool = field(default=True)
    logger: logging.Logger = field(
        default=get_default_logger("MasterConfigLogger"), repr=False, compare=False
    )

    def __post_init__(self):
        if self.debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

def load_config_from_yaml(file_path: str) -> MasterConfig:
    with open(file_path, "r") as file:
        config_data = yaml.safe_load(file)
    config = MasterConfig(**config_data)
    config.logger.info(f"Configuration loaded from {file_path}")
    return config
