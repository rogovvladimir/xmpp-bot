from .mycommands import command

@command('ping')
def pingHandler(unused):
    return 'pong'
