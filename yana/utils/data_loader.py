import json
from pathlib import Path
from typing import Any, Literal

from yana.domain.intents import Intent
from yana.domain.types import DataPairs
from yana.utils.text import strip_special_chars


def load_json(path: Path) -> Any:
    file = path.read_text()
    return json.loads(file)


def load_intent_train_test_pairs(path: Path) -> DataPairs:
    x_train: list[str] = []
    x_test: list[str] = []
    y_train: list[str] = []
    y_test: list[str] = []

    # Get the intents and sentences
    # { "intent": ["candidate", ...], ... }
    data: dict[str, list[str]] = load_json(path)

    for intent, candidates in data.items():
        for i, candidate in enumerate(candidates):
            print(intent, candidate)

            # Split the dataset in half
            if i % 2 == 0:
                y_test.append(intent)
                x_test.append(strip_special_chars(candidate))

            y_train.append(intent)
            x_train.append(strip_special_chars(candidate))

    return x_train, x_test, y_train, y_test


def load_intent_responses(path: Path) -> dict[Intent, list[str]]:
    # {intent: [],...}
    return load_json(path)


def load_intent_follow_ups(
    path: Path,
) -> dict[Literal["G1", "R1", "E0"] | Intent, list[str]]:
    return load_json(path)
