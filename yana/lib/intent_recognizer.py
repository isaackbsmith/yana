from pathlib import Path
import joblib
from sklearn.pipeline import Pipeline
from sentence_transformers import SentenceTransformer

from yana.domain.types import YANAConfig
from yana.utils.config import get_config
from yana.domain.logger import root_logger


class IntentRecognizer:
    def __init__(self, config: YANAConfig) -> None:
        self.config = config

        model_path = Path(self.config.intent_recognizer.paths.model)
        classifier_path = Path(self.config.intent_recognizer.paths.classifier)

        if model_path.exists() and classifier_path.exists():
            self.model = SentenceTransformer(str(model_path))
            self.classifier: Pipeline = joblib.load(classifier_path)
        else:
            raise FileNotFoundError("[IR] Could initialize intent recognizer")

    def predict_raw(self, sentence: list[str]):
        embeddings = self.model.encode(sentence, show_progress_bar=False)
        return self.classifier.predict(embeddings)

    def recognize(self, sentence: list[str]) -> str:
        root_logger.info("Recognizing intent")
        embeddings = self.model.encode(sentence, show_progress_bar=False)
        prediction = self.classifier.predict(embeddings)
        return prediction[0]



config = get_config()
INTENT_RECOGNIZER = IntentRecognizer(config)
