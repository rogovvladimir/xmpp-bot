import re

from . import BaseCommand, commands

from twilix.base.myelement import BreakStanza

class helpCommand(BaseCommand):
       
    COMMAND = u'help'
    HELP = u'get help'
    COMMAND_REGEX = re.compile(ur'^(?:help)?(.*)$')
    
    def chatHandler(self):
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
        reply = self.get_reply()
        reply.body = res
        return (reply, BreakStanza())
    
