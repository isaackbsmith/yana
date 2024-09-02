import asyncio
from pathlib import Path

from omegaconf import OmegaConf

from yana.domain.logger import root_logger
from yana.root.intent_recognizer import IntentRecognizer
from yana.root.speech_recognizer import SpeechRecognizer
from yana.root.speech_synthesizer import SpeechSynthesizer


async def main() -> None:
    # ROOT_PATH = Path().absolute()
    root_logger.info("[ROOT] Starting YANA")

    # Load configurations
    system_config = OmegaConf.load("yana/config/system_cfg.yml")
    silero_models_info = OmegaConf.load("yana/static/silero_models_info.yml")

    # Merge all configs
    config = OmegaConf.merge(system_config, silero_models_info)

    # Load resources
    tts = SpeechSynthesizer(config)
    ir = IntentRecognizer(config)
    stt = SpeechRecognizer(config)

    print(stt.listen())

if __name__ == "__main__":
    asyncio.run(main())
