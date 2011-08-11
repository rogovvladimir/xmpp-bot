import re

PTRN = r'''
            ([a-z]+)    # command part
        '''

REGEXP = re.compile(PTRN, re.VERBOSE)

def parsingCommand(line):
    if not line:
        return None
    m = REGEXP.match(line)
    return m.group(1) if m else None
