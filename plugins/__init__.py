from os import listdir, sep

for file in listdir(__name__ + sep):
    if file.startswith('plugin_') and file.endswith('.py'):
        __import__('%s.%s' % (__name__, file[:-3]), 
                   globals(), locals(), [], -1)

__all__ = ['mycommands']
