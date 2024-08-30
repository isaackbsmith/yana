from pathlib import Path
from omegaconf import OmegaConf

BASE_PATH = Path.cwd()
CONFIG_PATH = BASE_PATH / "yana/config/system_cfg.yml"

async def get_config():
    config = OmegaConf.load(CONFIG_PATH)
    return config

