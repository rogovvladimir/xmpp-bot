from twisted.internet import defer

from twilix import fields
from twilix.stanzas import Query, Iq

from .user import UserItemInfo
"""
class Item(VElement):
    elementName = 'item'
    #elementUri = 'http://jabber.org/protocol/muc#user'
    
    nick = fields.StringAttr('nick', required=False)
    role = fields.StringAttr('role', required=False)
    affiliation = fields.StringAttr('affiliation', required=False)
    jid = fields.StringAttr('jid', required=False)
    reason = fields.StringNode('reason', required=False)
"""

class AdminQuery(Query):
    
    elementUri = 'http://jabber.org/protocol/muc#admin'
    item = fields.ElementNode(UserItemInfo, required=False)

@defer.inlineCallbacks
def makeAdminQuery(item, iq, dispatcher):
    query = AdminQuery(item=item, parent=iq)
    query.iq.result_class = Iq
    dispatcher.send(query.iq)
    defr = query.iq.deferred
    defr.addCallback(querySuccess)
    defr.addErrback(queryError)
    res = yield defr
    defer.returnValue(res)
    
def querySuccess(defr):
    print '\nsuccess', unicode(defr)
    return True
        
def queryError(defr):
    print '\nfailed', defr.value.reason
    return False
