cmdcatalog = {}

class command(object):
    """An interface for addition elements in commands dictionary"""
    
    def __init__(self, cmd):
        """Constructor save name of new command"""
        self.name = cmd
        
    def __call__(self, func):
        """
        This method add handler for command and
        also add this pair in dictionary
        
        """
        cmdcatalog[self.name] = func
