import subprocess
from time import time
from pathlib import Path
from speech_recognition import AudioData

from yana.domain.types import YANAConfig
from yana.domain.logger import root_logger


class SpeechRecogizer:
    def __init__(self, config: YANAConfig) -> None:
        self.config = config
        self.whisper_model = Path(config.speech_recognizer.paths.whisper_model)
        self.user_audio = Path(config.speech_recognizer.paths.user_audio)
        self.whisper_binary = Path(config.speech_recognizer.paths.whisper_binary)

    def recognize_whisper(self) -> str:
        if not self.whisper_model.exists():
            raise FileNotFoundError(f"Wisper model {self.whisper_model} not found")

        full_command = f"./{self.whisper_binary} -m {self.whisper_model} -f {self.user_audio} -np -nt"

        # Execute shell command
        process = subprocess.Popen(
             full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        output, error = process.communicate()

        if error:
            raise Exception(f"Error processing audio: {error.decode("utf-8")}")

        # Process and return the output string
        decoded_str = output.decode("utf-8").strip()
        processed_str = decoded_str.replace("[BLANK_AUDIO]", "")

        return processed_str

    def recognize(self, audio: AudioData) -> str | None:
        root_logger.info("Recognizing speech")
        try:
            with self.user_audio.open(mode="wb") as f:
                f.write(audio.get_wav_data())

            start = time()
            output = self.recognize_whisper()
            end = time()
            root_logger.debug(f"Speech transcription took: {end - start} seconds")

            return output
        except Exception as e:
            root_logger.error(f"Transcription failed: {e}")

    def recognize_web(self, audio_path: Path) -> str:

        if not self.whisper_model.exists():
            raise FileNotFoundError(f"Wisper model {self.whisper_model} not found")

        full_command = f"./{self.whisper_binary} -m {self.whisper_model} -f {audio_path} -np -nt"

        # Execute shell command
        process = subprocess.Popen(
             full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        output, error = process.communicate()

        if error:
            raise Exception(f"Error processing audio: {error.decode("utf-8")}")

        # Process and return the output string
        decoded_str = output.decode("utf-8").strip()
        processed_str = decoded_str.replace("[BLANK_AUDIO]", "")

        return processed_str
