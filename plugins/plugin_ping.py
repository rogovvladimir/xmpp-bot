from .mycommands import command

from twilix.stanzas import Message
from twilix.base import WrongElement, BreakStanza

@command('ping')
class pingCommand(Message):
    
    def clean_body(self, value):
        if value != u'ping':
            raise WrongElement()
        return value
        
    def chatHandler(self):
        return (Message(from_=self.to,
                       to=self.from_,
                       type_=self.type_,
                       body=u'pong'), BreakStanza())

    HELP = u'check ur connection'
