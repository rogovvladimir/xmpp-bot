import os

from .mycommands import command
from .mycommands import cmdcatalog

@command('commands')
def commandsHandler(unused):
    cmdlist = [cmd for cmd in cmdcatalog]
    return 'Hello:) There are :\n[%s]\nlist of commands, supported by this bot' \
           % ', '.join(cmdlist)

