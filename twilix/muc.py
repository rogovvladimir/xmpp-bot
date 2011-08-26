from twilix.stanzas import Presence, Query
from twilix.base import VElement
from twilix import fields
from twilix.jid import internJID


class MultiChat(object):
    
    def __init__(self, dispatcher, room_jid):
        self.room_jid = room_jid
        self.dispatcher = dispatcher
        self.users = []

class MUCPresence(VElement):
    parentClass = Presence
    elementName ='x'
    
class ConnectPresence(MUCPresence):
    elementUri = 'http://jabber.org/protocol/muc'

class ItemInfo(VElement):
    elementName = 'item'
    elementUri = 'http://jabber.org/protocol/muc#user'

    affiliation = fields.StringAttr('affiliation', required=True)
    role = fields.StringAttr('role', required=True)

class UserItem(VElement):
    elementName = 'x'
    elementUri = 'http://jabber.org/protocol/muc#user'
    item = fields.ElementNode(ItemInfo, required=False)

class UserPresence(Presence):
    user = fields.ElementNode(UserItem, required=True)
    
    userroster = []
    
    def anyHandler(self):
        UserPresence.userroster.append(self.from_.resource)

def connection(dispatcher, client_jid, room_jid=None):    
    if room_jid is None:
        room_jid = 'vis@conference.jabber.ru/testa'
        #'joyful@conference.jabber.ru/testa'
    pres = Presence(to=room_jid, from_=client_jid)
    msg = ConnectPresence(parent=pres)
    #return msg.parent
    dispatcher.send(msg.parent)
