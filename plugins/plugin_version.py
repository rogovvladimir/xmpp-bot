import re

from . import BaseCommand

from twilix.jid import internJID, InvalidFormat
from twilix.base import WrongElement
#from twisted.internet import defer

class versionCommand(BaseCommand):
    
    COMMAND = u'version'
    HELP =  u"[with no parametrs, with 'me' parametr or any jabber id] \
show version's info"
    COMMAND_REGEX = re.compile(ur'^(version)(?: (me|.+))?$')
    
    def clean_body(self, value):
        super(type(self), self).clean_body(value)
        param = self.cmdpars.group(2)
        if not param:
            self.jid = self.host.client_jid
        elif param == u'me':
            self.jid = self.from_
        else:
            try:
                self.jid = internJID(param)
            except InvalidFormat:
                raise WrongElement
        return value
    
    #@defer.inlineCallbacks
    def commandHandler(self):
        defr = self.host.version.getVersion(self.jid)
        defr.addCallback(makeMessage, self.jid)
        defr.addErrback(makeErrormessage, self.jid)
        return defr
        #res = yield defr
        #defer.returnValue(res)
        
def makeMessage(defr, jid):
    res = u"%s client's information :\nname : %s \nversion : %s\nos \
: %s"      % (jid,defr.client_name, defr.client_version, defr.client_os)                       
    return res

def makeErrormessage(defr, jid):
    res = u'Impossible to get %s version, because [%s]'\
            % (jid, defr.value.reason)
    return res
