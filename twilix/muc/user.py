from pydispatch import dispatcher

from twilix.stanzas import Presence
from twilix.base import VElement
from twilix import fields

class UserItemInfo(VElement):
    """
    Class for user info from xml message
    """
    elementName = 'item'
    elementUri = 'http://jabber.org/protocol/muc#user'

    affiliation = fields.StringAttr('affiliation', required=False)
    role = fields.StringAttr('role', required=False)
    nick = fields.StringAttr('nick', required=False)
    jid = fields.JidAttr('jid', required=False)
    
    reason = fields.StringNode('reason', required=False)

class UserItem(VElement):
    """
    Class container for user info
    """
    elementName = 'x'
    elementUri = 'http://jabber.org/protocol/muc#user'
    item = fields.ElementNode(UserItemInfo, required=False)

class UserPresence(Presence):
    """Class for multi chat occupant's info"""   
        
    user = fields.ElementNode(UserItem, required=False)
    
    def anyHandler(self):
        """
        Saves list of info about active users in rooms
        """
                
        if self.user is None:
            return
        
        room_jid = self.from_.bare()
        if room_jid not in self.host.roster:
            return
        
        self.host.roster[room_jid] = filter(lambda el: el.from_.resource != self.from_.resource, self.host.roster[room_jid])
        
        if self.type_ == 'unavailable':
            dispatcher.send(self.host.user_unavailable, user=self)
        else:
            self.host.roster[room_jid].append(self)
            dispatcher.send(self.host.user_available, user=self)
            
            
        print 'ROSTER', self.host.roster
