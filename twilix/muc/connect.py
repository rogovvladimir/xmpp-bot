from twilix.stanzas import Presence
from twilix.base import VElement


class ConnectPresence(VElement):
    parentClass = Presence
    elementName ='x'
    elementUri = 'http://jabber.org/protocol/muc'
    
