from pathlib import Path
import joblib
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sentence_transformers import SentenceTransformer

from yana.utils.data_loader import load_json


BASE_PATH = Path("yana/static/intents").resolve()
model_path = Path(BASE_PATH / "intent_model")
intents_path = Path(BASE_PATH / "intents.pkl")
embeddings_path = Path(BASE_PATH / "intent_embeddings.pkl")
classifier_path = Path(BASE_PATH / "intent_classifier.pkl")
data_path = Path(BASE_PATH / "intents.json")


# Load data
def load_intent_pairs(path: Path) -> tuple[list[str], list[str]]:
    sentences: list[str] = []
    intents: list[str] = []

    # Get the intents and sentences
    # { "intent": ["candidate", ...], ... }
    data: dict[str, list[str]] = load_json(path)

    for intent, candidates in data.items():
        for candidate in candidates:
            print(intent, candidate)
            intents.append(intent)
            sentences.append(candidate)

    return intents, sentences


def main() -> None:
    # Load and save model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    model.save(str(model_path))

    # Get intent-sentence pairs
    intents, sentences = load_intent_pairs(data_path)

    # Compute embeddings
    print("Encoding data")
    embeddings = model.encode(sentences, batch_size=10)

    # Save embeddings and intents
    print("Saving embeddings and intents")
    joblib.dump(embeddings, embeddings_path)
    joblib.dump(intents, intents_path)

    # Create and train Support Vector Classifier (SVC)
    print("Training classifier")
    classifier = make_pipeline(StandardScaler(), SVC(kernel="linear"))
    classifier.fit(embeddings, intents)

    # Save tained classifier
    print("Saving classifier")
    joblib.dump(classifier, classifier_path)


if __name__ == "__main__":
    print("Started training intent recognition model")
    main()
    print("Finished training intent recognition model")
