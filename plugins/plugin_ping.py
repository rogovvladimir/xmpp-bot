import re

from . import BaseCommand

class pingCommand(BaseCommand):
    
    COMMAND = u'ping'
    HELP = u'check ur connection'
    COMMAND_REGEX = re.compile(ur'^(ping)$')
    
    def commandHandler(self):
        return self.makeReply(u'pong')


