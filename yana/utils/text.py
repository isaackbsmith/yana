import string


def strip_special_chars(text: str) -> str:
    # Delete all punctuation from the string
    translator = text.maketrans("", "", string.punctuation)
    return text.translate(translator).lower()
