import functools
from pathlib import Path
from collections.abc import Callable
from speech_recognition import AudioData, Recognizer, Microphone

from yana.domain.types import YANAConfig
from yana.domain.logger import root_logger
from yana.lib.speech_recognizer import SpeechRecogizer
from yana.utils.config import get_config
from yana.utils.text import strip_special_chars


class SpeechListener:
    def __init__(self, config: YANAConfig, stt: SpeechRecogizer) -> None:
        self.microphone = Microphone(
            sample_rate=config.speech_listener.params.sample_rate
        )
        self.recognizer = Recognizer()
        self.user_audio = Path(config.speech_listener.paths.user_audio)
        self.stt = stt

    def listen(self) -> str | None:
        root_logger.info("[STT] Listening...")
        try:
            with Microphone(sample_rate=config.speech_listener.params.sample_rate) as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source)
            result = self.stt.recognize(audio)
            if not result:
                return None
            root_logger.info(f"Transcription: {result}")
            return strip_special_chars(result)
        except Exception as e:
            root_logger.error(f"[STT] Transcription failed: {e}")

    def bg_callback(
        self,
        recognizer: Recognizer,
        audio: AudioData,
        call_next: Callable | None = None,
    ) -> None:
        try:
            root_logger.info("[STT::BG] Recognizing...")
            result = self.stt.recognize(audio)
            if call_next is not None and result is not None:
                call_next(result)
        except Exception as e:
            root_logger.error(f"[STT] Background transcription failed: {e}")

    def listen_in_background(self, call_next: Callable) -> Callable:
        # Apply the caller's callback to the internal callback
        callback = functools.partial(self.bg_callback, call_next=call_next)

        # Calibrate once, and start listening
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

        root_logger.info("[STT::BG] Listening...")
        return self.recognizer.listen_in_background(self.microphone, callback)


config = get_config()
stt = SpeechRecogizer(config)
SPEECH_LISTENER = SpeechListener(config, stt)
