
DEBUG_LEVEL_PAGE = False
DEBUG_LEVEL_DOCUMENT = True

def debug_message_page(*message):
    if DEBUG_LEVEL_PAGE:
        print(*message)

def debug_message_document(*message):
    if DEBUG_LEVEL_DOCUMENT:
        print(*message)