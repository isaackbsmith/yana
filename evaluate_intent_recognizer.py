from pathlib import Path

from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from yana.lib.intent_recognizer import INTENT_RECOGNIZER
from yana.utils.data_loader import load_intent_train_test_pairs


BASE_PATH = Path("yana/static/ir").resolve()
data_path = Path(BASE_PATH / "intents.json")


def main() -> None:
    _, X_test, _, y_test = load_intent_train_test_pairs(data_path)

    y_pred = INTENT_RECOGNIZER.predict_raw(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average="macro")
    recall = recall_score(y_test, y_pred, average="macro")
    f1 = f1_score(y_test, y_pred, average="macro")

    print(f"Accuracy: {accuracy:.2f}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1-score: {f1:.2f}")


if __name__ == "__main__":
    main()
