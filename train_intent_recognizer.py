from pathlib import Path
import joblib
from sklearn.svm import LinearSVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sentence_transformers import SentenceTransformer

from yana.utils.data_loader import load_intent_train_test_pairs


BASE_PATH = Path("yana/static/intents").resolve()
model_path = Path(BASE_PATH / "intent_model")
intents_path = Path(BASE_PATH / "intents.pkl")
embeddings_path = Path(BASE_PATH / "intent_embeddings.pkl")
classifier_path = Path(BASE_PATH / "intent_classifier.pkl")
data_path = Path(BASE_PATH / "intents.json")


def main() -> None:
    # Load and save model
    model = SentenceTransformer("all-MiniLM-L6-v2")
    model.save(str(model_path))

    # Get intent-sentence pairs
    X_train, _, y_train, _ = load_intent_train_test_pairs(data_path)

    # Compute embeddings
    print("Encoding data")
    X_embeddings = model.encode(X_train, batch_size=10)

    # Save embeddings and intents
    print("Saving embeddings and intents")
    joblib.dump(X_embeddings, embeddings_path)
    joblib.dump(y_train, intents_path)

    # Create and train Support Vector Classifier (SVC)
    print("Training classifier")
    classifier = make_pipeline(StandardScaler(), LinearSVC())
    classifier.fit(X_embeddings, y_train)

    # Save tained classifier
    print("Saving classifier")
    joblib.dump(classifier, classifier_path)


if __name__ == "__main__":
    print("Started training intent recognition model")
    main()
    print("Finished training intent recognition model")
