from pydispatch import dispatcher

from twilix.stanzas import Presence, Iq
from twilix.base import VElement, MyElement, EmptyStanza
from twilix import fields
from twilix.jid import internJID

from .user import UserPresence, UserItemInfo
from .connect import ConnectPresence
from .admin import makeAdminQuery
    
class MultiChat(object):
    """
    Class implements multi chat user extension
    """
           
    user_available = object()
    user_unavailable = object()
    
    default_room = 'vis@conference.jabber.ru'
    default_nick = 'testa'
    
    def __init__(self, dispatcher):
        """Setup global configuration"""
        self.dispatcher = dispatcher
        
    def init(self):
        self.roster = {}
        self.dispatcher.registerHandler((UserPresence, self))
        
    def enter_room(self, presence, room_jid=default_room, nickname=default_nick):
        """
        Sends presence which allows client to enter the room
        
        :param room_jid: JID of room-conference
        :param nickname: string-type client's nickname in conference
        :param status: string-type client's status message
        """
        reciever = internJID(room_jid)
        
        assert reciever.bare() not in self.roster, 'already in room'
        
        reciever.resource = nickname
 
        presence = MyElement.makeFromElement(presence)
        presence = Presence.createFromElement(presence)
 
        presence.to = reciever
        presence.from_ = self.dispatcher.myjid
        #presence.type_ = 'available'
        
        msg = ConnectPresence(parent=presence)
        
        self.roster[reciever.bare()] = []
        
        self.dispatcher.send(msg.parent)
        
    def leave_room(self, presence, room_jid=default_room, nickname=default_nick):
        """
        Sends presence which leaves client from the room
        
        :param room_jid: JID of room-conference
        :param nickname: string-type client's nickname in conference
        """
        reciever = internJID(room_jid)
        
        assert reciever.bare() in self.roster, 'not in room'
        
        reciever.resource = nickname
        
        presence = MyElement.makeFromElement(presence)
        presence = Presence.createFromElement(presence)
        
        presence.to = reciever
        presence.from_ = self.dispatcher.myjid
        presence.type_ = 'unavailable'
        
        msg = ConnectPresence(parent=presence)
        
        self.dispatcher.send(msg.parent)
        
        del self.roster[reciever.bare()]
        
    def set_affiliation(self, room_jid=default_room, 
                            jid='whitegoose@jabber.ru', 
                            affiliation='outcast', reason=None):
        reciever = internJID(room_jid)
        iq = Iq(type_='set', to=reciever, from_=self.dispatcher.myjid)
        i = UserItemInfo(jid=internJID(jid), affiliation=affiliation, reason=reason)
        return makeAdminQuery(i, iq, self.dispatcher)
        
    def set_role(self, room_jid=default_room, nick='whitegoose', 
                        role='none', reason=None):
        reciever = internJID(room_jid)
        iq = Iq(type_='set', to=reciever, from_=self.dispatcher.myjid)
        i = UserItemInfo(nick=nick, role=role, reason=reason)
        return makeAdminQuery(i, iq, self.dispatcher) 
        


