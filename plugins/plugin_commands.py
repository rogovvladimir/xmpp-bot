import os

from .mycommands import command
from .mycommands import cmdcatalog

@command('commands')
def commandsHandler(unused):
    cmdlist = [cmd for cmd in cmdcatalog]
    return 'There are :\n[%s]\n commands, supported by this bot' \
           % ',\n'.join(cmdlist)

