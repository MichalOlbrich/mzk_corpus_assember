import re

from corpus_creation.debug_module import debug_message_page

# Czech letters + digits
CZECH_CHARS = r"a-zA-ZáÁčČďĎéÉěĚíÍňŇóÓřŘšŠťŤúÚůŮýÝžŽ0-9„“"

REGULAR_CHARS = CZECH_CHARS + r"\s\.\,\-\–\—\!\\\?\;\:\(\)\/"  # allow long dash etc.


BREAK_CHARS = r"[\-\–\—\‒\−\﹣\－\¬\«\u00AD]"
def fix_expanded_hyphenation(text):
    # remove hyphen-like characters at end of line, then join lines
    return re.sub(BREAK_CHARS + r"+\s*\n\s*", "", text)


def is_page_useless(page, lines):
    """Return True for pages that are TOC-like or mostly OCR artifacts."""

    debug_message_page("PAGEE CHAR LEN:", len(page.strip()))
    # 1) Extremely short page → useless
    if len(page.strip()) < 150:
        return True

    # 2) Count Czech letters
    czech_letters = re.findall(f"[{CZECH_CHARS}]", page)
    czech_ratio = len(czech_letters) / max(len(page), 1)

    # 2a) If Czech ratio < 50%, it's mostly garbage/noise
    if czech_ratio < 0.5:
        # print("czech_ratio < 0.5")
        return True

    # 3) TOC detection: lots of dot leaders ("..... 23")
    dot_leader_lines = sum(
        1 for l in lines if re.search(r"\.{3,}.*$", l.strip())
    )
    if dot_leader_lines >= 4:  # having ≥4 strongly indicates a TOC page
        # print("dot_leader_lines")
        return True

    # 4) Count lines that contain Czech text
    czech_lines = sum(1 for l in lines if re.search(f"[{CZECH_CHARS}]", l))

    # If page has >10 lines but only 1–2 lines with real text → useless
    if len(lines) > 10 and czech_lines <= 2:
        # print("has >10 lines but only 1–2 lines")
        return True

    # 5) Percentage of “regular” characters (letters or at least punctuation)
    allowed_chars = re.findall(f"[{REGULAR_CHARS}]", page)
    regular_ratio = len(allowed_chars) / len(page)

    # If < 95% of characters are normal (rest = symbols ⧘⧛◊□ etc.)
    # for most pages its close to 99,99% so everything below 98 % is sus
    # print("regular_ratio", regular_ratio)
    if regular_ratio < 0.96:
        # print("< 96% of characters are normal")
        return True

    # 6) Uppercase ratio
    letters = re.findall(r"[A-Za-zÁČĎÉĚÍŇÓŘŠŤÚŮÝŽáčďéěíňóřšťúůýž]", page)
    uppercase_letters = [ch for ch in letters if ch.isupper()]

    if letters:  # avoid division by zero
        uppercase_ratio = len(uppercase_letters) / len(letters)
        if uppercase_ratio > 0.5:
            # print("> 50% Uppercase ratio")
            return True

    return False