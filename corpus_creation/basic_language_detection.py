

def is_czech_by_chars(text, given_ratio=0.003):
    czech_diacritics = "áéíóúýčďěňřšťůžÁÉÍÓÚÝČĎĚŇŘŠŤŮŽ"
    count = sum(1 for ch in text if ch in czech_diacritics)
    ratio = count / max(1, len(text))

    # print("RATIO:",ratio,"\tCOUNT:",count)

    if ratio > given_ratio:          # > 1% - 10% normal Czech, so 1% is still very generous
        return True
    return False
