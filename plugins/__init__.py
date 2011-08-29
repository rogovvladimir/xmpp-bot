import os
from twilix.stanzas import Message
from twilix.muc.delay import Delay
from twilix import fields
from twilix.base import WrongElement, DeclarativeFieldsMetaClass, BreakStanza, EmptyStanza

commands = []

class MetaCommand(DeclarativeFieldsMetaClass):
    def __init__(cls, name, bases, dct):
        if 'COMMAND' in dct:
            commands.append(cls)
        super(MetaCommand, cls).__init__(name, bases, dct)

class BaseCommand(Message):
    __metaclass__ = MetaCommand
    
    delay = fields.ElementNode(Delay, required=False)
    
    def clean_body(self, value):
        if not value:
            raise WrongElement()
        cmd_check = self.COMMAND_REGEX.search(value)
        if cmd_check is None:
            raise WrongElement()
        self.cmdpars = cmd_check
        return value
        
    def makeReply(self, res):
        if res is None:
            reply = EmptyStanza()
        else:
            reply = self.get_reply()
            reply.body = res
            if self.type_ == 'groupchat':
                reply.to = reply.to.bare()
        return (reply, BreakStanza())
    
    def anyHandler(self):
        if self.delay is not None:
            return self.makeReply(None)
        else:
            return self.commandHandler()

def register(dispatcher, host):
    helpcommand = None
    for cmd in commands:
        if cmd.COMMAND != u'help':
            dispatcher.registerHandler((cmd, host))
        else:
            helpcommand = cmd
        
    dispatcher.registerHandler((helpcommand, host))
    return True
    

dir =  os.path.dirname(__file__)

for file in os.listdir(__name__ + os.sep):
    if not file.startswith('plugin_') or \
       not (file.endswith('.py') or 
            os.path.isdir(os.path.join(dir, file))):
                continue
    if file.endswith('.py'):
        file = file[:-3]
    __import__('%s.%s' % (__name__, file), 
                globals(), locals(), [], -1)
