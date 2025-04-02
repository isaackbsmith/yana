import re
from yana.domain.entities import NamedEntity
from yana.domain.types import InteractionPrompts, NamedEntities, YANAConfig
from yana.domain.logger import root_logger
from yana.lib.entity_recognizer import ENTITY_RECOGNIZER
from yana.lib.speech_listener import SPEECH_LISTENER
from yana.lib.speech_synthesizer import SPEECH_SYNTHESIZER


def interpolate_response(text: str, placeholder: str, value: str) -> str:
    formatted_response = text.replace(f"{{{placeholder}}}", value)
    root_logger.info(f"Formatted Response: {formatted_response}")
    return formatted_response


def process_response(response: str, values: dict[str, str]) -> str:
    print(values)
    # Extract placeholder
    extractor = r"\{(.*?)\}"
    match = re.findall(extractor, response)

    if not match:
        return response

    # Match on the placeholder
    for placeholder in match:
        # Get value and interpolate it into response
        value = values.get(placeholder)

        if not value:
            continue

        root_logger.info(f"Response processor detected value: {value}")
        response = interpolate_response(response, placeholder, value)
    return response


def get_yes_no(reply: str) -> str:
    yes_variants = ["yes", "yeah", "yep", "sure", "okay", "ok", "affirmative"]
    no_variants = ["no", "nope", "no please", "nah", "never", "absolutely not"]

    # Check if the user response contains any "yes" variants
    for yes_variant in yes_variants:
        if yes_variant in reply:
            return "yes"

    # Check if the user response contains any "no" variants
    for no_variant in no_variants:
        if no_variant in reply:
            return "no"

    return "unknown"


def get_entity(config: YANAConfig,
               field: str,
               entity: NamedEntity,
               entities: NamedEntities) -> str:
    # Prompts
    prompts: InteractionPrompts = {
        "ask": "Please provide the {field}",
        "confirm": "Did you say the {field} is {value}?",
        "success": "{value} has been recorded as {field}",
        "unknown": "I'm sorry, I do not understand what {value} means",
        "failure": "Sorry, I could not process what you said",
    }

    # Return the first entity that is reconized by default
    # TODO: The NER module can recognize vague words so remove them
    if entities and entities[entity]:
        first_entity = entities[entity][0]
        root_logger.info(f"Entity provided by user: {first_entity}")
        return first_entity

    # Ask the user for the missing information
    ask = process_response(prompts["ask"], {"field": field})
    SPEECH_SYNTHESIZER.speak([ask])
    response = SPEECH_LISTENER.listen()

    if not response:
        # If the user says nothing, start over
        failure = process_response(prompts["failure"], {})
        SPEECH_SYNTHESIZER.speak([failure])
        return get_entity(config, field, entity, None)

    # Recognize the new entities provided by the user
    new_entities = ENTITY_RECOGNIZER.recognize(response)
    new_entity = new_entities.get(entity) if new_entities else None
    root_logger.info(f"Recognized entity: {new_entity}")

    if not new_entity:
        # Repeat process if the entity is not recognized
        unknown = process_response(prompts["unknown"], {"value": response})
        SPEECH_SYNTHESIZER.speak([unknown])
        return get_entity(config, field, entity, None)

    # Confirm that the new entity is what the user intended
    confirm = process_response(prompts["confirm"], {"field": field, "value": new_entity[0]})
    print(confirm)
    SPEECH_SYNTHESIZER.speak([confirm])

    while True:
        reply = SPEECH_LISTENER.listen()
        if not reply:
            # Exit if user says nothing
            root_logger.info("User did not reply to yes or no question")
            SPEECH_SYNTHESIZER.speak(["Sorry, I did not hear a yes or a no"])
        else:
            yes_no = get_yes_no(reply)
            match yes_no:
                case "yes":
                    # The user has confirmed the entity so reuturn it
                    root_logger.info("User replied in the affirmative")
                    success = process_response(prompts["success"], {"field": field, "value": new_entity[0]})
                    SPEECH_SYNTHESIZER.speak([success])
                    return new_entity[0]
                case "no":
                    # Restart process if the user declines the entity
                    root_logger.info("User replied in the negative")
                    SPEECH_SYNTHESIZER.speak(["Alright, let's take this again"])
                    return get_entity(config, field, entity, None)
                case "unknown":
                    # Ask for yes or no again
                    root_logger.info("User reply is neither yes nor no")
                    SPEECH_SYNTHESIZER.speak(["Sorry, I did not hear a yes or a no"])
