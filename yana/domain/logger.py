import json
import logging
import logging.config
from pathlib import Path


BASE_PATH = Path.cwd()
LOG_CONFIG_PATH = "yana/config/log_cfg.json"


def setup_logger(name: str = "root", level: int = logging.INFO) -> logging.Logger:
    config_file = BASE_PATH / LOG_CONFIG_PATH

    with open(config_file) as conf:
        config = json.load(conf)
    logging.config.dictConfig(config)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    return logger


root_logger = setup_logger("root")
api_logger = setup_logger("api")
reminder_logger = setup_logger("reminder")
