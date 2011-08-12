from .mycommands import command

@command('ping')
def pingHandler():
    return 'pong'
