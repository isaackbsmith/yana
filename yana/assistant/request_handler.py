from yana.domain.intents import Intent
from yana.domain.models.assistant import AudioResponseSchema
from yana.domain.types import NamedEntities, YANAConfig
from yana.assistant.paths import interaction_path_map, general_interaction_path
from yana.domain.logger import root_logger


async def handle_request(config: YANAConfig, intent: str, entities: NamedEntities, web: bool = False) -> AudioResponseSchema | None:
    recongized_intent = Intent.try_from_str(intent)
    # Get the conversation path if it exists in the map else go to the default path
    root_logger.info("Determining interaction path")
    path = interaction_path_map.get(recongized_intent, general_interaction_path)
    try:
        root_logger.debug(f"Interaction path found: {path.__name__}")
        print(f"Interaction path found: {path.__name__}")
        result = await path(config, recongized_intent, entities, web)
        return result
    except Exception as e:
        root_logger.exception(f"Request handler error occurred: {e}")
