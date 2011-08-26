from twilix.stanzas import Presence
from twilix.base import VElement
from twilix import fields

class UserItemInfo(VElement):
    elementName = 'item'
    elementUri = 'http://jabber.org/protocol/muc#user'

    affiliation = fields.StringAttr('affiliation', required=True)
    role = fields.StringAttr('role', required=True)

class UserItem(VElement):
    elementName = 'x'
    elementUri = 'http://jabber.org/protocol/muc#user'
    item = fields.ElementNode(UserItemInfo, required=False)

class User(object):
    def __init__(self, nick, role, affiliation):
        self.nick = nick
        self.role = role
        self.affiliation = affiliation
        
    def __unicode__(self):
        return unicode(self.__dict__)

class UserPresence(Presence):
    user = fields.ElementNode(UserItem, required=True)
    
    def anyHandler(self):
        self.host.userroster.append(User(self.from_.resource, 
                                    self.user.item.role,
                                    self.user.item.affiliation))
