import re

# Czech letters + digits
CZECH_CHARS = r"a-zA-ZáÁčČďĎéÉěĚíÍňŇóÓřŘšŠťŤúÚůŮýÝžŽ0-9„“"

# Allowed punctuation around words
ALLOWED_PUNCTUATION = r"\(\)\[\]:;,.!?-"

def is_standard_word(word):
    """
    Return True if the word contains only Czech letters, digits,
    or allowed punctuation around it.
    """
    # Remove leading/trailing allowed punctuation
    stripped = word.strip(ALLOWED_PUNCTUATION + " ")

    # Check if core contains only Czech letters or digits
    pattern = f"^[{CZECH_CHARS}]+$"
    return bool(re.match(pattern, stripped))
