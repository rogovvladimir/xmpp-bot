from twilix.stanzas import Presence
from twilix.base import VElement
from twilix import fields

class UserItemInfo(VElement):
    """
    Class for user info from xml message
    """
    elementName = 'item'
    elementUri = 'http://jabber.org/protocol/muc#user'

    affiliation = fields.StringAttr('affiliation', required=True)
    role = fields.StringAttr('role', required=True)

class UserItem(VElement):
    """
    Class container for user info
    """
    elementName = 'x'
    elementUri = 'http://jabber.org/protocol/muc#user'
    item = fields.ElementNode(UserItemInfo, required=False)

class User(object):
    """
    Class for user's info
    
    Attributes : 
        
        nick -- nickname of room's occupant
        
        role -- role of room's occupant
        
        affiliation -- affiliation of room's occupant
    
    """
    def __init__(self, nick, role, affiliation):
        self.nick = nick
        self.role = role
        self.affiliation = affiliation
        
    def __repr__(self):
        return unicode(self.__dict__)

class UserPresence(Presence):
    """Class for multi chat occupant's info"""
    user = fields.ElementNode(UserItem, required=True)
    
    def anyHandler(self):
        """
        Saves list of info about active users in room
        """
        user = User(self.from_.resource, 
                    self.user.item.role,
                    self.user.item.affiliation)
        
                    
        if self.type_ == 'unavailable':
            self.host.userroster = filter(lambda el: el.nick != user.nick, self.host.userroster)
        else:
            self.host.userroster.append(user)
