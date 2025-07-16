import re


def format_editorial(text: str) -> str:
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text.strip())

    # Smart punctuation
    text = text.replace(" .", ".").replace(" ,", ",")
    text = text.replace(" :", ":").replace(" ;", ";")

    # Capitalize first letter
    if text and text[0].islower():
        text = text[0].upper() + text[1:]

    # Fix common AI quirks
    text = text.replace("Here's an improved version:", "").replace("Rewritten:", "")
    return text.strip()
