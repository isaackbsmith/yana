import asyncio

from yana.assistant.request_handler import handle_request
from yana.domain.logger import root_logger
from yana.lib.entity_recognizer import ENTITY_RECOGNIZER
from yana.lib.intent_recognizer import INTENT_RECOGNIZER
from yana.lib.speech_listener import SPEECH_LISTENER
from yana.utils.config import get_config
from yana.utils.text import strip_special_chars


async def main() -> None:
    root_logger.info("[YANA] Initializing core modules")
    config = get_config()

    async def process_request(request: str | None) -> None:
        root_logger.info(f"User Request: {request}")

        if request is None:
            return

        root_logger.info("Extracting intent and entities")
        clean_request = strip_special_chars(request)
        intent = INTENT_RECOGNIZER.recognize([clean_request])
        entities = ENTITY_RECOGNIZER.recognize(clean_request)

        root_logger.info(
            f"Message: {clean_request}\n, Intent: {intent}\n, Entities: {entities}\n"
        )

        try:
            await handle_request(config, intent, entities)
        except Exception as e:
            root_logger.error(f"An error occurred: {e}")

    while True:
        try:
            user_request = SPEECH_LISTENER.listen()
            await process_request(user_request)
        except KeyboardInterrupt:
            raise SystemExit()


if __name__ == "__main__":
    asyncio.run(main())
