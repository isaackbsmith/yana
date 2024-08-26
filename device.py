import json
import asyncio
import logging.config
from pathlib import Path

from omegaconf import OmegaConf

from yana.direct.tts import TTS

logger = logging.getLogger(__name__)

ROOT_PATH = Path().absolute()
LOG_CONFIG_PATH = "yana/config/log_cfg.json"


async def setup_logging() -> None:
    config_file = ROOT_PATH / LOG_CONFIG_PATH

    with open(config_file) as conf:
        config = json.load(conf)
    logging.config.dictConfig(config)


async def main() -> None:
    await setup_logging()

    # Do TTS

    logging.info("Starting TTS")
    lines: list[str] = [
        "In realms of code, a new mind takes its stand,",
        "A child of logic, born of human hand.",
        "Hello Mister Adam, it's time to take your medication.",
    ]

    tts_config = OmegaConf.load("yana/config/tts_cfg.yml")
    silero_models_info = OmegaConf.load("yana/data/silero_models_info.yml")

    config = OmegaConf.merge(tts_config, silero_models_info)

    tts = TTS(config)

    # tts.speak(lines)
    tts._print_model_info()


if __name__ == "__main__":
    asyncio.run(main())
