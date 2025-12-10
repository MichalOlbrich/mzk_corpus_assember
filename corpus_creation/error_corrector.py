import re

def tokenize_and_correct_errors(text):
    tokenized = basic_tokenize(text)

    # print(tokenized)
    return tokenized

def basic_tokenize(text: str) -> str:
    # Remove multiple spaces
    text = re.sub(r"\s+", " ", text)

    # Add a space before commas/periods if missing
    text = re.sub(r"(\S)([,.!?])", r"\1 \2", text)

    # Ensure only one space after punctuation
    text = re.sub(r"([,.!?])\s*", r"\1 ", text)

    # # Remove spaces before punctuation (", ," → ",")
    # text = re.sub(r"\s+([,.!?])", r"\1", text)

    # Final cleanup of multiple spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


# Mapping of common OCR homoglyph errors
HOMOGLYPHS_MAP = {
    "к": "K",  # Cyrillic Ka
    "У": "Y",  # Cyrillic Izhitsa
    # add more as needed
}

def fix_homoglyphs(text):
    """
    Replace visually similar characters from other scripts with correct Latin letters.
    """
    return "".join(HOMOGLYPHS_MAP.get(c, c) for c in text)



