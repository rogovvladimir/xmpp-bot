from time import localtime, strftime

from .mycommands import command

@command('time')
def timeHandler(unused):
    return strftime("%a, %d %b %Y, %H:%M:%S", localtime())
