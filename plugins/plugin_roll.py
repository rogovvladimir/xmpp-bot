from random import randint

from .mycommands import command

@command('roll')
def rollHandler(): 
    return randint(1, 6)
