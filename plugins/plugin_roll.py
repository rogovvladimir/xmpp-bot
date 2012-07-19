import re
from random import randint

from . import BaseCommand

from twilix.base.myelement import BreakStanza

class rollCommand(BaseCommand):
    
    COMMAND = u'roll'
    HELP = u'random number between 1 to 6 (or integer parametr)'
    COMMAND_REGEX = re.compile(ur'^(roll)(?: ([1-9][0-9]*))?$')
        
    def chatHandler(self):
        param = self.cmdpars.group(2)
        self.bound = int(param) if param else 6
        res = randint(1, self.bound)
        reply = self.get_reply()
        reply.body = res
        return (reply, BreakStanza())
    
    def groupchatHandler(self):
        param = self.cmdpars.group(2)
        self.bound = int(param) if param else 6
        res = randint(1, self.bound)
        reply = self.get_reply()
        reply.body = u'%s: %s' %(reply.to.resource, res)
        reply.to = reply.to.bare()
        return (reply, BreakStanza())
