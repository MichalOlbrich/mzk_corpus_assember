import re
from corpus_creation import error_corrector, basic_page_cleaner, basic_line_cleaner, basic_language_detection, error_corrector
from corpus_creation.debug_module import debug_message_page, debug_message_document


def cleanup_and_create_decade_corpus(documents, file_names):
    clean_documents = []
    clean_f_names= []
    cnt_not_czech = 0
    cnt_fracture = 0
    cnt_almost_not_czech = 0
    not_used_docs = 0
    for i, (document, f_name) in enumerate( zip(documents,file_names)):
        # if i != 66:
        #     continue
        # if i < 65:
        #     continue
        debug_message_document(f"document {i} out of {len(documents)}")
        if not basic_language_detection.is_czech_by_chars(document):
            debug_message_document("NOT CZECH:", cnt_not_czech)
            cnt_not_czech+=1
            continue
        elif basic_language_detection.is_fracture(document,given_ratio=0.015):
            debug_message_document("FRACTURE:", cnt_fracture)
            cnt_fracture += 1
            continue
        clean_doc = clean_document(document)
        if not basic_language_detection.is_czech_by_chars(clean_doc, given_ratio=0.01):
            if len(clean_doc) > 1000:
                debug_message_document("ALMOST NOT CZECH:", cnt_almost_not_czech)
                cnt_almost_not_czech+=1
                # weird_documents.append(clean_doc)
            else:
                not_used_docs += 1
                debug_message_document("TOO SHORT", not_used_docs)
            continue
        clean_doc = error_corrector.tokenize_and_correct_errors(clean_doc)
        # print(clean_doc)

        clean_documents.append(clean_doc)
        clean_f_names.append(f_name)

    return clean_documents, clean_f_names , [cnt_not_czech, cnt_fracture, cnt_almost_not_czech, not_used_docs]


def clean_document(document):
    cnt_non_standard = 0
    cnt_non_standard_pages = 0
    pattern_page_separator = r"-{13}<Page:\s*\d+\s*>-{11,}"
    # Split the document at these tags
    pages = re.split(pattern_page_separator, document)
    # The text before the first page marker is usually empty → remove it
    pages = [p.strip() for p in pages if p.strip()]
    clean_pages = []
    for i, page in enumerate(pages):
        lines = page.split("\n")
        debug_message_page(f"{i} #################################################")
        if i >= len(pages)-2 or i <= 1:
            continue
        if basic_page_cleaner.is_page_useless(page, lines):
            debug_message_page("----PAGE IS USELESS------#################################################")
            cnt_non_standard_pages+=1
            continue
        cleaned_lines = []
        debug_message_page("#################################################")
        for line in lines:
            # Remove BOM if present
            line = line.lstrip("\ufeff").strip()
            if not line:
                continue
            # Skip page numbering lines
            if basic_line_cleaner.is_page_number_line(line):
                continue
            if basic_line_cleaner.is_non_word_line(line):
                continue
            if basic_line_cleaner.is_tab_line(line):
                continue
            cleaned_lines.append(line)

        # FIX HYPHENATION HERE
        cleaned_page = "\n".join(cleaned_lines)
        cleaned_page = basic_page_cleaner.fix_expanded_hyphenation(cleaned_page)
        cleaned_page = error_corrector.fix_homoglyphs(cleaned_page)

        debug_message_page(cleaned_page)

        clean_pages.append(cleaned_page)
    document = "\n".join(clean_pages)
    return document

    # ## DEBUG
    #     lines = cleaned_page.split("\n")
    #     for line in lines:
    #         words = line.split()
    #         for word in words:
    #             if not is_standard_word(word):
    #                 cnt_non_standard+=1
    #                 # debug_message("NONSTANDARD:\t",word)
    #
    #         #debug_message(line)
    #
    #
    #     # Now debug_message or store the cleaned page text
    #     #cleaned_page = "\n".join(cleaned_lines)
    #     debug_message(cleaned_page)
    #
    # debug_message("cnt_non_standard",cnt_non_standard)
    # debug_message("cnt_non_standard",cnt_non_standard_pages)
