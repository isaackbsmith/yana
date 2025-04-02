from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForTokenClassification

from yana.utils.config import get_config


tokenizer = AutoTokenizer.from_pretrained("d4data/biomedical-ner-all")

model = AutoModelForTokenClassification.from_pretrained("d4data/biomedical-ner-all")


ner_pipe = pipeline(
    "ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple"
)


if __name__ == "__main__":
    config = get_config()
    # Save model and tokenizer for later use
    model.save_pretrained(config.NER.paths.model)
    tokenizer.save_pretrained(config.NER.paths.tokenizer)
