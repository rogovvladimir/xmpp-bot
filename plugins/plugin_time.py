import re
from time import localtime, strftime

from . import BaseCommand


class timeCommand(BaseCommand):

    COMMAND = u'time'
    HELP = u'show ur time'
    COMMAND_REGEX = re.compile(ur'^(time)$')
        
    def commandHandler(self):
        res = strftime(u"%a, %d %b %Y, %H:%M:%S", localtime())
        return self.makeReply(res)
        
