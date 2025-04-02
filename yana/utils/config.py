from omegaconf import OmegaConf

from yana.domain.types import YANAConfig


def get_config() -> YANAConfig:
    sys_cfg = OmegaConf.load("yana/config/system_cfg.yml")
    silero_models_info = OmegaConf.load("yana/static/silero_models_info.yml")

    # Merge all configs
    config = OmegaConf.merge(sys_cfg, silero_models_info)
    return config


def get_test_config() -> YANAConfig:
    config = OmegaConf.load("yana/config/test_cfg.yml")
    return config
