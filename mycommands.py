
import random
import time 

commands = {}

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
        commands[self.name] = func
        

@command('ping')
def pingHandler():
    body = 'pong'
    return body

@command('roll')
def rollHandler():
    body = random.randint(1, 6)
    return body
    
@command('time')
def timeHandler():
    body = time.strftime("%a, %d %b %Y, %H:%M:%S", time.localtime())
    return body
    
@command('commands')
def commandsHandler():
    body = 'There are :\n[%s]\n commands, supported by this bot' \
           % ',\n'.join([cmd for cmd in commands])
    return body
