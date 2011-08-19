import os
from twilix.stanzas import Message
from twilix.base import WrongElement, DeclarativeFieldsMetaClass

commands = []

class MetaCommand(DeclarativeFieldsMetaClass):
    def __init__(cls, name, bases, dct):
        if 'COMMAND' in dct:
            commands.append(cls)
        super(MetaCommand, cls).__init__(name, bases, dct)

class BaseCommand(Message):
    __metaclass__ = MetaCommand
    
    def clean_body(self, value):
        if not value:
            raise WrongElement()
        cmd_check = self.COMMAND_REGEX.search(value)
        if cmd_check is None:
            raise WrongElement()
        self.cmdpars = cmd_check
        return value

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
