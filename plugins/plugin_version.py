from .mycommands import command

@command('version')
def versionHandler(chatmessage):
    versionclass = chatmessage.host.version
    return '\nversion : %s\nname : %s\nos : %s' % \
            (versionclass.client_version, versionclass.client_name,
            versionclass.client_os)
    
