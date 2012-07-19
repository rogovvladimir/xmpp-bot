import re
from time import localtime, strftime

from . import BaseCommand

from twilix.base.myelement import BreakStanza

class timeCommand(BaseCommand):

    COMMAND = u'time'
    HELP = u'show ur time'
    COMMAND_REGEX = re.compile(ur'^(time)$')
        
    def chatHandler(self):
        res = strftime(u"%a, %d %b %Y, %H:%M:%S", localtime())
        reply = self.get_reply()
        reply.body = res
        return (reply, BreakStanza())
    
    def groupchatHandler(self):
        res = strftime(u"%a, %d %b %Y, %H:%M:%S", localtime())
        reply = self.get_reply()
        reply.body = u'%s: %s' %(reply.to.resource, res)
        reply.to = reply.to.bare()
        return (reply, BreakStanza())
