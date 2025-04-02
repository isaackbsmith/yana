from pathlib import Path
from typing import Any
from pydantic import BaseModel


class AudioResponseModel(BaseModel):
    transcription: str | None
    response: str | None
    audio: Any | None

class AudioResponseSchema(BaseModel):
    response: str | None
    audio: Path
