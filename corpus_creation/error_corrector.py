import re

def tokenize_and_correct_errors(text):
    tokenized = basic_tokenize(text)
    tokenized = replace_wrong_ocr_letters(tokenized)
    # print(tokenized)
    return tokenized

def basic_tokenize(text: str) -> str:
    # Remove multiple spaces
    # text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[ \t]+", " ", text)

    # word followed by non-word (except whitespace)
    text = re.sub(r"(\w)([^\w\s])", r"\1 \2", text)
    # non-word followed by word (except whitespace)
    text = re.sub(r"([^\w\s])(\w)", r"\1 \2", text)
    text = re.sub(r"([^\w\s])([^\w\s])", r"\1 \2", text)
    # # Remove spaces before punctuation (", ," → ",")
    # text = re.sub(r"\s+([,.!?])", r"\1", text)

    # Final cleanup of multiple spaces
    text = re.sub(r" +", " ", text).strip()

    return text

def replace_wrong_ocr_letters(text: str) -> str:
    text = re.sub(r" y ", " v ", text)
    text = re.sub(r" Y ", " V ", text)
    text = re.sub(r"\nY ", "\nV ", text)


    text = re.sub(r"[■|*/\\^<>]", "", text)
    text = re.sub(r"(?<!\.\s) K ", " k ", text)
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



