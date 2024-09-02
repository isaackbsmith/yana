from pathlib import Path
import subprocess
from time import time
from speech_recognition import Recognizer, Microphone

from yana.domain.types import YANAConfig
from yana.domain.logger import root_logger


class SpeechRecognizer:
    def __init__(self, config: YANAConfig) -> None:
        self.config = config
        self.vosk_model = Path(config.STT.paths.vosk_model)
        self.whisper_model = Path(config.STT.paths.whisper_model)
        self.user_audio = Path(config.STT.paths.user_audio)
        self.whisper_binary = Path(config.STT.paths.whisper_binary)


    def process_audio(self) -> str:
        if not self.whisper_model.exists():
            raise FileNotFoundError(f"Wisper model not found")

        full_command = f"./{self.whisper_binary} -m {self.whisper_model} -f {self.user_audio} -np -nt"

        # Execute shell command
        process = subprocess.Popen(full_command,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        output, error = process.communicate()

        if error:
            raise Exception(f"Error processing audio: {error.decode("utf-8")}")

        # Process and return the output string
        decoded_str = output.decode("utf-8").strip()
        processed_str = decoded_str.replace("[BLANK_AUDIO]", "")

        return processed_str


    def use_whisper(self) -> str | None:
        try:
            recognizer = Recognizer()
            microphone = Microphone(sample_rate=16000)

            with microphone as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

                with self.user_audio.open(mode="wb") as f:
                    f.write(audio.get_wav_data())

                start = time()
                output = self.process_audio()
                end = time()
                root_logger.debug(f"Speech transcription took: {end - start} seconds")
                return output
        except Exception as e:
            root_logger.error(f"Transcription failed: {e}")

    def use_vosk(self) -> None:
        raise NotImplementedError("Vosk is not available")

    def listen(self, vosk = False) -> str | None:
        root_logger.info("Listening...")

        if vosk:
            result = self.use_vosk()
        else:
            result = self.use_whisper()

        root_logger.info(f"User: {result}")
        return result


