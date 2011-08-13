import os

dir =  os.path.dirname(__file__)

for file in os.listdir(__name__ + os.sep):
    if not file.startswith('plugin_') or \
       not (file.endswith('.py') or 
            os.path.isdir(os.path.join(dir, file))):
                continue
    if file.endswith('.py'):
        file = file[:-3]
    __import__('%s.%s' % (__name__, file), 
                globals(), locals(), [], -1)

__all__ = ['mycommands']
