from twilix.stanzas import Presence
from twilix.base import VElement
from twilix import fields
from twilix.jid import internJID

from user import UserPresence
from connect import ConnectPresence
    
class MultiChat(object):
    """
    Class implements multi chat user extension
    """
    
    default_room = 'vis@conference.jabber.ru'
    default_nick = 'testa'
    
    def __init__(self, dispatcher):
        """Setup global configuration"""
        self.dispatcher = dispatcher
        
    def init(self):
        self.roster = {}
        self.dispatcher.registerHandler((UserPresence, self))
        
    def enter_room(self, room_jid=default_room, nickname=default_nick, status=None):
        """
        Sends presence which allows client to enter the room
        
        :param room_jid: JID of room-conference
        :param nickname: string-type client's nickname in conference
        :param status: string-type client's status message
        """
        reciever = internJID(room_jid)
        
        reciever.resource = nickname
        
        pres = Presence(to=reciever, from_=self.dispatcher.myjid, status=status)
        msg = ConnectPresence(parent=pres)
        
        self.roster[reciever.bare()] = []
        
        self.dispatcher.send(msg.parent)
        
    def leave_room(self, room_jid=default_room, nickname=default_nick):
        """
        Sends presence which leaves client from the room
        
        :param room_jid: JID of room-conference
        :param nickname: string-type client's nickname in conference
        """
        reciever = internJID(room_jid)
        reciever.resource = nickname
        
        pres = Presence(to=reciever, from_=self.dispatcher.myjid, type_='unavailable')
        msg = ConnectPresence(parent=pres)
        
        self.dispatcher.send(msg.parent)
        self.roster.remove(reciever.bare())
