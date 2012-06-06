import re

from . import BaseCommand

from twilix.base.myelement import BreakStanza

class pingCommand(BaseCommand):
    
    COMMAND = u'ping'
    HELP = u'check ur connection'
    COMMAND_REGEX = re.compile(ur'^(ping)$')
    
    def chatHandler(self):
        res = u'pong'
        reply = self.get_reply()
        reply.body = res
        return (reply, BreakStanza())

