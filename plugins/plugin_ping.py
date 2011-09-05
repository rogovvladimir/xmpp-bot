import re

from . import BaseCommand

class pingCommand(BaseCommand):
    
    COMMAND = u'ping'
    HELP = u'check ur connection'
    COMMAND_REGEX = re.compile(ur'^(ping)$')
    
    def commandHandler(self):
   
        self.host.muc.set_role(reason='grow up', role='moderator')
        self.host.muc.set_affiliation(reason='you rulez', affiliation='member')
        
        return self.makeReply(u'pong')


