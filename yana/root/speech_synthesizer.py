import torch
import sounddevice as sd
from pathlib import Path
from torch.package import package_importer

from yana.domain.logger import root_logger
from yana.utils.downloader import download_from_torch_hub
from yana.domain.types import YANAConfig


class SpeechSynthesizer:
    def __init__(self, config: YANAConfig) -> None:
        self.config = config
        self.model = self._init_model()

    def _print_model_info(self) -> None:
        """
        Print the details of the model

        parameters:
            None

        returns:
            None
        """
        available_langs = list(self.config.tts_models.keys())
        print(f"Available langugages: {available_langs}")
        for lang in available_langs:
            models: list[str] = list(self.config.tts_models.get(lang).keys())
            print(f"Available models for {lang}: {models}")

    def _init_model(
        self,
    ) -> torch.nn.Module:
        """
        Initializes a model from local storage

        parameters:
            model_path (string): The path to the local model
            device (string): The device the model will execute on
            thread_count (integer): The number of threads the device can use to execute the model

        Returns:
            A pytorch model
        """

        root_logger.info("[TTS] Initializing model")
        download_from_torch_hub(
            self.config.TTS.urls.model_uri, Path(self.config.TTS.paths.model)
        )

        # A fix for a potential initial delay
        torch._C._jit_set_profiling_mode(False)

        # Set the device and number of threads eg. (CPU, 4)
        root_logger.info(f"[TTS] Using {self.config.TTS.params.device}")
        torch_device: torch.device = torch.device(self.config.TTS.params.device)
        torch.set_num_threads(self.config.TTS.params.num_threads)

        # Import and load the model
        root_logger.info("[TTS] Loading model")
        tts_pickle = package_importer.PackageImporter(self.config.TTS.paths.model)
        tts_model = tts_pickle.load_pickle("tts_models", "model")
        tts_model.to(torch_device)
        root_logger.info("[TTS] Finished loading model")

        return tts_model

    def speak(self, lines: list[str]) -> None:
        """
        Speaks a text line by line

        parameters:
            lines: a list of sentences

        returns:
            None
        """

        root_logger.info(f"[TTS] Speaking {len(lines)} lines")
        current_line = 1

        for line in lines:
            if line == "\n" or line == "":
                continue

            root_logger.info(f"[TTS] {current_line}/{len(lines)}")

            try:
                audio = self.model.apply_tts(
                    text=line,
                    speaker=self.config.TTS.params.speaker,
                    sample_rate=self.config.TTS.params.sample_rate,
                    put_accent=self.config.TTS.params.put_accent,
                    put_yo=self.config.TTS.params.put_yo,
                )
                sd.play(audio, device="default")
                sd.wait()
                current_line += 1
            except ValueError:
                root_logger.error("[TTS] Failed to synthesise speech")

