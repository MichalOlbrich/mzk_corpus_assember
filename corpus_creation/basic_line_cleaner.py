import re

from datasets.data_files import NON_WORDS_CHARS

PAGE_NUMBER_PATTERN = r"^[\-\–—\s]*\d+[\-\–—\s]*$"
ROMAN_PATTERN = r"^[\-\–—\s]*[IVXLCDMivxlcdm]+\.[\-\–—\s]*$"
ROMAN_NODOT_PATTERN = r"^[\-\–—\s]*[IVXLCDMivxlcdm]+[\-\–—\s]*$"


def is_page_number_line(line):
    """Return True if the line is likely a page-number line, including mis-OCRed characters."""

    stripped = line.strip()

    # 1. Strong regex matches
    if re.match(PAGE_NUMBER_PATTERN, stripped):
        return True
    if re.match(ROMAN_PATTERN, stripped):
        return True
    if re.match(ROMAN_NODOT_PATTERN, stripped):
        return True

    # ------------------------------------------------------------------
    # 2. Heuristics: short line + limited content
    # ------------------------------------------------------------------

    # If the line is short (≤ 10 chars), it may be numbering
    if len(stripped) <= 10:

        # Keep only alphanumerics for the core test
        core = re.sub(r"[^A-Za-z0-9]", "", stripped)

        if not core:
            return True  # line is only punctuation/dashes → header/footer

        # A. Pure digits → page number
        if core.isdigit():
            return True

        # B. Pure letters → page number (OCR often substitutes)
        # Accept 1–3 letter sequences (X, G, S, B, i, l, O …)
        if re.fullmatch(r"[A-Za-z]{1,3}", core):
            return True

        # C. Mixed digit/letter but very small (e.g., "6G")
        if len(core) <= 3 and core.isalnum():
            return True

    return False


# characters you consider "word" characters (letters + digits)
WORD_CHARS = r"[A-Za-z0-9ÁáČčĎďÉéĚěÍíŇňÓóŘřŠšŤťÚúŮůÝýŽž„!“]"
word_re = re.compile(WORD_CHARS)

def is_non_word_line(line, threshold=0.4):
    # stripped = line.strip()
    # if not stripped:
    #     return True
    stripped = line
    total = len(stripped)
    word_chars = len(word_re.findall(stripped))
    non_word_chars = total - word_chars

    # If no word chars, definitely non-word
    if word_chars == 0:
        return True

    # If most characters are garbage symbols → non-word line
    if non_word_chars / total > threshold:
        # print("NON-WORD LINE:", stripped)
        return True

    return False

def is_tab_line(line):
    if re.match(".+\t.+", line):
        # print("TAB LINE:", line)
        return True
    return False