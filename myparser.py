import re

PTRN = r'''
            ([a-z]+)    # command part
        '''

REGEXP = re.compile(PTRN, re.VERBOSE)

def parsingCommand(line):
    m = REGEXP.match(line)
    return m.group(1) if m else None
