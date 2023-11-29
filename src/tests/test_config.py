import os
import pytest
import tempfile
import logging
from src.config import MasterConfig, load_config_from_yaml


def test_master_config_defaults():
    config = MasterConfig()
    assert config.port == 5000
    assert config.debug is True


def test_master_config_custom():
    config = MasterConfig(port=8000, debug=False)
    assert config.port == 8000
    assert config.debug is False


def test_load_config_from_yaml():
    with tempfile.NamedTemporaryFile("w", delete=False) as tmp:
        yaml_content = """
        port: 6000
        debug: False
        """
        tmp.write(yaml_content)
        tmp_path = tmp.name

    config = load_config_from_yaml(tmp_path)

    assert config.port == 6000
    assert config.debug is False

    os.remove(tmp_path)


def test_logging_level():
    config_debug = MasterConfig(debug=True)
    assert config_debug.logger.getEffectiveLevel() == logging.DEBUG

    config_info = MasterConfig(debug=False)
    assert config_info.logger.getEffectiveLevel() == logging.INFO
