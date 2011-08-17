cmdcatalog = {}

help = u'commands'

class command(object):
    """An interface for addition elements in commands dictionary"""
    
    def __init__(self, cmd):
        """Constructor save name of new command"""
        self.name = cmd
        
    def __call__(self, handler):
        """
        This method add handler for command and
        also add this pair in dictionary
        
        """
        cmdcatalog[self.name] = handler 


def register(dispatcher, host):
    for cmd in cmdcatalog:
        if cmd != u'commands':
            dispatcher.registerHandler((cmdcatalog[cmd], host))
        
    dispatcher.registerHandler((cmdcatalog['commands'], host))
    return True
            
