from time import localtime, strftime

from .mycommands import command, help

from twilix.stanzas import Message
from twilix.base import WrongElement, BreakStanza

@command('time')
class timeCommand(Message):
    
    def clean_body(self, value):
        if value != u'time':
            raise WrongElement
        return value
        
    def chatHandler(self):
        res = strftime(u"%a, %d %b %Y, %H:%M:%S", localtime())
        return (Message(from_=self.to,
                       to=self.from_,
                       type_=self.type_,
                       body=res), BreakStanza())
    HELP = u'show ur time'
