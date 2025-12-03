import os
import re


def load_decade(path):

    files = [f for f in os.listdir(path)
             if os.path.isfile(os.path.join(path, f))]

    # Optional: keep only .txt files (remove this filter if not needed)
    files = [f for f in files if f.lower().endswith(".ocr")]

    if not files:
        print("No OCR files found.")
        return []

    # Load all files into a list
    documents = []
    for fname in files:
        with open(os.path.join(path, fname), "r", encoding="utf-8") as f:
            documents.append(f.read())

    # Display first file
    print(f"--- Showing first file: {files[0]} ---\n")
    clean_document(documents[2])

    return documents


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

# Characters that indicate a broken word at line end
BROKEN_END_CHARS = [
    "-", "–", "—", "-", "‒", "−", "﹣", "－", "­", "«", "¬"
]
# Build a regex like: ([-–—-‒−﹣－­«¬])
BROKEN_END_RE = "[" + re.escape("".join(BROKEN_END_CHARS)) + "]"


def fix_hyphenation(lines):
    """
    Join lines where the word is broken across lines using hyphens,
    soft hyphens, or OCR garbage characters.
    """
    fixed = []
    buffer = ""

    for line in lines:
        stripped = line.rstrip()

        # 1. If previous line ended with a hyphen-like char, merge
        if buffer:
            # Remove trailing hyphen-like characters from buffer
            buffer = re.sub(BROKEN_END_RE + r"+$", "", buffer)
            # Append the current line without leading spaces
            buffer += stripped.lstrip()
            fixed.append(buffer)
            buffer = ""
            continue

        # 2. If this line ends with a break character → store in buffer
        if re.search(BROKEN_END_RE + r"+$", stripped):
            buffer = stripped
            continue

        # 3. Otherwise keep the line normally
        fixed.append(stripped)

    # If buffer still contains something (rare), append it
    if buffer:
        fixed.append(buffer)

    return fixed

BREAK_CHARS = r"[\-\–\—\‒\−\﹣\－\¬\«\u00AD]"
def fix_expanded_hyphenation(text):
    # remove hyphen-like characters at end of line, then join lines
    return re.sub(BREAK_CHARS + r"+\s*\n\s*", "", text)


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

def clean_document(document):
    cnt_non_standard = 0
    pattern = r"-{13}<Page:\s*\d+\s*>-{11,}"
    page_number_pattern = r"^[\-\–—\s]*\d+[\-\–—\s]*$"
    roman_pattern = r"^[\-\–—\s]*[IVXLCDMivxlcdm]+\.[\-\–—\s]*$"

    # Split the document at these tags
    pages = re.split(pattern, document)
    # The text before the first page marker is usually empty → remove it
    pages = [p.strip() for p in pages if p.strip()]

    for page in pages:
        lines = page.split("\n")
        cleaned_lines = []
        print("++++++++++++++++++++++++++")
        for line in lines:
            # Remove BOM if present
            line = line.lstrip("\ufeff").strip()
            if not line:
                continue
            # Skip page numbering lines
            if is_page_number_line(line):
                continue
            cleaned_lines.append(line)


        # FIX HYPHENATION HERE
        cleaned_page = "\n".join(cleaned_lines)
        cleaned_page = fix_expanded_hyphenation(cleaned_page)
        cleaned_page = fix_homoglyphs(cleaned_page)

        lines = cleaned_page.split("\n")
        for line in lines:
            words = line.split()
            for word in words:
                if not is_standard_word(word):
                    cnt_non_standard+=1
                    print("NONSTANDARD:\t",word)

            print(line)


        # Now print or store the cleaned page text
        # cleaned_page = "\n".join(cleaned_lines)
        # print(cleaned_page)

    print("cnt_non_standard",cnt_non_standard)
