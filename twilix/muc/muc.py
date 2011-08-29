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
    def __init__(self, dispatcher, jid):
        """Setup global configuration"""
        self.dispatcher = dispatcher
        self.client_jid = jid
        
    def init(self):
        self.userroster = []
        self.dispatcher.registerHandler((UserPresence, self))
        
    def enter_room(self, room_jid='vis@conference.jabber.ru', nickname='noxyu', status=None):
        """
        Sends presence which allows client to enter the room
        
        :param room_jid: JID of room-conference
        :param nickname: string-type client's nickname in conference
        """
        reciever = internJID(room_jid)
        reciever.resource = nickname
        
        pres = Presence(to=reciever, from_=self.client_jid, status=status)
        msg = ConnectPresence(parent=pres)
        
        self.dispatcher.send(msg.parent)
