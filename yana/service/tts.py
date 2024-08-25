import logging
import torch
import sounddevice as sd
from pathlib import Path
from torch.package import package_importer
from omegaconf import DictConfig, ListConfig

from yana.utils.downloader import download_from_torch_hub


class TTS:
    def __init__(self, config: ListConfig | DictConfig) -> None:
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

        logging.info("Initializing TTS model")
        download_from_torch_hub(
            self.config.urls.model_uri, Path(self.config.paths.model_path)
        )

        # A fix for a potential initial delay
        torch._C._jit_set_profiling_mode(False)

        # Set the device and number of threads eg. (CPU, 4)
        logging.info(f"Using {self.config.params.device}")
        torch_device: torch.device = torch.device(self.config.params.device)
        torch.set_num_threads(self.config.params.num_threads)

        # Import and load the model
        logging.info("Loading model")
        tts_pickle = package_importer.PackageImporter(self.config.paths.model_path)
        tts_model = tts_pickle.load_pickle("tts_models", "model")
        tts_model.to(torch_device)
        logging.info("Finished loading model")

        return tts_model

    def speak(self, lines: list[str]) -> None:
        """
        Speaks a text line by line

        parameters:
            lines: a list of sentences

        returns:
            None
        """

        logging.info(f"Speaking {len(lines)} lines")
        current_line = 1

        for line in lines:
            if line == "\n" or line == "":
                continue

            logging.info(f"{current_line}/{len(lines)}")

            try:
                audio = self.model.apply_tts(
                    text=line,
                    speaker=self.config.params.speaker,
                    sample_rate=self.config.params.sample_rate,
                    put_accent=self.config.params.put_accent,
                    put_yo=self.config.params.put_yo,
                )
                sd.play(audio, device="default")
                sd.wait()
                current_line += 1
            except ValueError:
                logging.error("Failed to synthesise speech")
