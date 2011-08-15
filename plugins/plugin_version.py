from .mycommands import command
from twilix.stanzas import Message

import re

PTRN = r'''
            <name>(?P<name>.*)</name>
            <version>(?P<version>.*)</version>
            (?:<os>(.*)</os>)?
        '''

REGEXP = re.compile(PTRN, re.VERBOSE)


@command('version')
def versionHandler(chatmessage):
    iq = chatmessage.host.version.getVersion(chatmessage.from_, 
                                                None)
    defr = chatmessage.host.dispatcher.send(iq)
    defr.addCallback(makeMessage, chatmessage.to, chatmessage.from_, chatmessage.type_)
    return defr


def makeMessage(defr, from_, to, type_):
    m = REGEXP.search(str(defr.__dict__))
    res = "Ur client's information :\nname : %s \
            \nversion : %s\nos : %s"  % m.groups()                        
    message = Message(from_=from_,
                            to=to,
                            type_=type_,
                            body=res)
    return message
