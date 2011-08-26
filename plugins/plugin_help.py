import re

from . import BaseCommand, commands

from twilix.base import EmptyStanza, BreakStanza

class helpCommand(BaseCommand):
       
    COMMAND = u'help'
    HELP = u'get help'
    COMMAND_REGEX = re.compile(ur'^(?:help)?(.*)$')
    
    def commandHandler(self):
        if self.type_ == 'groupchat' and self.cmdpars.group(1):
            reply = (EmptyStanza(), BreakStanza())
        else:
            res = u''
            cmnd = self.cmdpars.group(1)
            if cmnd:
                res = u'[%s] is a bad command for me' % self.cmdpars.group()
            helpdict = {}
            for cmd in commands:
                helpdict[cmd.COMMAND] = getattr(cmd, 'HELP', 
                                        u"(haven't help for this command)")
            res += u'\nThere are :\n\t%s\nlist of \
commands, supported by this bot' % \
                                        '\n\t'.join(['[%s] -- %s;' % \
                                                (cmd, helpdict[cmd]) \
                                           for cmd in sorted(helpdict)])
            reply = self.makeReply(res)
        return reply
    
