from pathlib import Path
import joblib
from sklearn.pipeline import Pipeline
from sentence_transformers import SentenceTransformer

from yana.domain.types import YANAConfig


class IntentRecognizer:
    def __init__(self, config: YANAConfig) -> None:
        self.config = config

        model_path = Path(self.config.IR.paths.model)
        classifier_path = Path(self.config.IR.paths.classifier)

        if model_path.exists() and classifier_path.exists():
            self.model = SentenceTransformer(str(model_path))
            self.classifier: Pipeline = joblib.load(classifier_path)
        else:
            raise FileNotFoundError("[IR] Could initialize intent recognizer")

    def recognize(self, sentence: list[str]) -> str:
        embeddings = self.model.encode(sentence, show_progress_bar=False)
        return self.classifier.predict(embeddings)

