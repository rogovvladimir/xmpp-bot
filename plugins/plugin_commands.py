from .mycommands import command
from .mycommands import cmdcatalog

from twilix.stanzas import Message
from twilix.base import WrongElement

@command('commands')
class commandsCommand(Message):
    def clean_body(self, value):
        self.badcommand = value if value != u'commands' else u''
        return value
    def chatHandler(self):
        res = u''
        if self.badcommand:
            res = u'[%s] is a bad command for me' % self.badcommand
        res += u'\nThere are :\n\t%s\nlist of commands, supported by this bot' \
                % '\n\t'.join(['[%s] -- %s' %(cmd, cmdcatalog[cmd].HELP) for cmd in cmdcatalog])
        return Message(from_=self.to,
                       to=self.from_,
                       type_=self.type_,
                       body=res)
    HELP = u'get help'
