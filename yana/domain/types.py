from collections.abc import Awaitable, Callable
from typing import Literal
from omegaconf import DictConfig, ListConfig

from yana.domain.intents import Intent
from yana.domain.entities import NamedEntity
from yana.domain.models.assistant import AudioResponseSchema


YANAConfig = ListConfig | DictConfig

DataPairs = tuple[list[str], list[str], list[str], list[str]]

NamedEntities = dict[NamedEntity, list[str]] | None

ConversationPath = Callable[[YANAConfig, Intent, NamedEntities, bool], Awaitable[AudioResponseSchema | None]]

InteractionPrompts = dict[Literal["ask", "confirm", "success", "unknown", "failure"], str]
