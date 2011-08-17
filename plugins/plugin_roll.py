from random import randint

from .mycommands import command, help

from twilix.stanzas import Message
from twilix.base import WrongElement, BreakStanza

@command('roll')
class rollCommand(Message):
    
    def clean_body(self, value):
        if not value.startswith(u'roll'):
            raise WrongElement
        param = value[4:]
        if not param:
            self.bound = 6
        elif not param[1:] or not param[1:].isdigit() or not int(param[1:]):
            raise WrongElement
        else:
            self.bound = int(param[1:])
        return value
        
    def chatHandler(self):
        res = randint(1, self.bound)
        return (Message(from_=self.to,
                       to=self.from_,
                       type_=self.type_,
                       body=res), BreakStanza())
    
    HELP = u'random number between 1 to 6 (or integer parametr)'
