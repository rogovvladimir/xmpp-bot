from .mycommands import command

from twilix.jid import internJID, InvalidFormat

from twilix.stanzas import Message
from twilix.base import WrongElement, BreakStanza

from twisted.internet import defer

@command('version')
class versionCommand(Message):
    
    def clean_body(self, value):
        if not value.startswith(u'version'):
            raise WrongElement()
        jid = value[7:]
        if not jid:
            self.jid = self.host.client_jid
        elif jid == u' me':
            self.jid = self.from_
        elif jid.startswith(u' ') and jid[1:]:
            try:
                self.jid = internJID(jid[1:])
            except InvalidFormat:
                raise WrongElement()
        else:
            raise WrongElement()
        
        return value
    
    @defer.inlineCallbacks
    def chatHandler(self):
        defr = self.host.version.getVersion(self.jid)
        defr.addCallback(makeMessage, self.jid)
        defr.addErrback(makeErrormessage, self.jid)
        res = yield defr
        message = Message(from_=self.to,
                           to=self.from_,
                           type_=self.type_,
                           body=res)
        defer.returnValue((message,BreakStanza()))
        
    HELP =  u"[with no parametrs, with 'me' parametr or any jabber id] show version's info"

def makeMessage(defr, jid):
    res = u"%s client's information :\nname : %s \nversion : %s\nos : %s"\
            % (jid,
               defr.client_name, defr.client_version, defr.client_os)                       
    return res

def makeErrormessage(defr, jid):
    res = u'Impossible to get %s version, because [%s]'\
            % (jid, defr.value.reason)
    return res
