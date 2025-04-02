from pathlib import Path
import random
from yana.domain.intents import Intent
from yana.domain.models.assistant import AudioResponseSchema
from yana.domain.types import NamedEntities, YANAConfig
from yana.lib.speech_listener import SpeechListener
from yana.lib.speech_recognizer import SpeechRecogizer
from yana.lib.speech_synthesizer import SpeechSynthesizer
from yana.utils.conversation import get_yes_no
from yana.utils.data_loader import load_intent_follow_ups, load_intent_responses


async def general_interaction_path(config: YANAConfig, intent: Intent, entities: NamedEntities, web: bool) -> AudioResponseSchema | None:
    responses = load_intent_responses(Path(config.interaction.paths.responses))
    follow_ups = load_intent_follow_ups(Path(config.interaction.paths.follow_ups))

    tts = SpeechSynthesizer(config)
    stt = SpeechRecogizer(config)
    listener = SpeechListener(config, stt)

    # Get random response
    response = random.choice(responses[intent])
    print(response)

    if web:
        return tts.respond_web(response)

    # Select random response from either a generic follow up
    # or a specific follow up
    r1 = random.choice(follow_ups["G1"])
    r2 = random.choice(follow_ups.get(intent, "Would you like to do something else?"))
    follow_up = random.choice([r1, r2])

    tts.speak([response, follow_up])

    wait = [True, False]
    if random.choice(wait):
        # Wait for yes or no
        wait_for_response = True
        while wait_for_response:
            phrase = listener.listen()
            if not phrase:
                tts.speak(["Sorry, I did not hear what you said"])
            else:
                match get_yes_no(phrase):
                    case "yes":
                        yes_response = random.choice(follow_ups["R1"])
                        tts.speak([yes_response])
                        wait_for_response = False
                    case "no":
                        no_response = random.choice(follow_ups["E0"])
                        tts.speak([no_response])
                        wait_for_response = False
                    case "unknown":
                        tts.speak(["Sorry, I did not hear a yes or a no"])
