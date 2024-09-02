import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    file = path.read_text()
    return json.loads(file)
