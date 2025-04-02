from collections import defaultdict
from typing import Any, cast
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForTokenClassification

from yana.domain.entities import NamedEntity
from yana.domain.types import NamedEntities, YANAConfig
from yana.utils.config import get_config
from yana.domain.logger import root_logger


class NamedEntityRecognizer:
    def __init__(self, config: YANAConfig) -> None:
        self.config = config
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.config.entity_recognizer.paths.tokenizer
        )
        self.model = AutoModelForTokenClassification.from_pretrained(
            self.config.entity_recognizer.paths.model
        )
        self.ner_pipe = pipeline(
            "ner",
            model=self.model,
            tokenizer=self.tokenizer,
            aggregation_strategy="simple",
        )

    def format_entities(self, entities: Any) -> NamedEntities:
        result = defaultdict(list)
        for entity in entities:
            result[NamedEntity.try_from_str(entity["entity_group"])].append(
                entity["word"]
            )
        return cast(NamedEntities, dict(result))


    def recognize(self, text: str) -> NamedEntities:
        root_logger.info("Recognizing entities")
        entities = self.ner_pipe(text)
        entities = cast(Any, entities)

        if not entities:
            return

        return self.format_entities(entities)


config = get_config()
ENTITY_RECOGNIZER = NamedEntityRecognizer(config)
