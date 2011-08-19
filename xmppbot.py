"""
Module is an example of simple chat bot for any xmpp-server
"""
import twisted.words.protocols.jabber.client as twisted_client
from twisted.internet import threads, defer, reactor
from twisted.words.protocols.jabber.xmlstream import XmlStreamFactory
from twisted.words.protocols.jabber import xmlstream
from twisted.names.srvconnect import SRVConnector
from pydispatch import dispatcher

from twilix.stanzas import Message, Iq, Presence
from twilix.base import WrongElement
from twilix.jid import internJID
from twilix.dispatcher import Dispatcher
from twilix.version import ClientVersion
from twilix.disco import Disco
from twilix.roster import Roster

import plugins

import ConfigParser
from optparse import OptionParser

class XMPPClientConnector(SRVConnector):
    """Pre-connect initialization for client connector"""
    def __init__(self, reactor, domain, factory, port):
        self.port = port
        SRVConnector.__init__(self, reactor, 'xmpp-client', 
                              domain, factory)
                              
"""class describes handler for <chat> type stanzas"""
"""class ChatMessage(Message):
    def clean_body(self, value):
        cmd = myparser.parsingCommand(value)
        if cmd not in mycommands.cmdcatalog:
            cmd = mycommands.help
        return cmd
    
    @defer.inlineCallbacks
    def chatHandler(self):
        res = yield mycommands.cmdcatalog[self.body](self)
        message = Message(from_=self.to,
                              to=self.from_,
                              type_=self.type_,
                              body=res)
        defer.returnValue(message)
"""
    
class Client(object):
    """main class for client to server connection"""

    def __init__(self, reactor, client_jid, server, secret, port):
        """Setup handler and connect to server"""
        self.reactor = reactor
        self.client_jid = client_jid

        a = twisted_client.XMPPAuthenticator(client_jid, secret)
        self.f = XmlStreamFactory(a)
        
        #set handlers for xmlstream's events
        self.f.addBootstrap(xmlstream.STREAM_CONNECTED_EVENT, 
                            self.onConnected)
        self.f.addBootstrap(xmlstream.STREAM_END_EVENT, 
                            self.onDisconnected)
        self.f.addBootstrap(xmlstream.STREAM_AUTHD_EVENT, 
                            self.onAuthenticated)
        self.f.addBootstrap(xmlstream.INIT_FAILED_EVENT, 
                            self.onInitFailed)

        self.connector = XMPPClientConnector(reactor, server, 
                                             self.f, port)
        self.connector.connect()

        self.xmlstream = None

    #handlers for xmlstream's events

    def onConnected(self, xs):
        """
        xmlstream.STREAM_CONNECTED_EVENT handler.
        Calls when client connected to server
        """
        
        self.xmlstream = xs
        self.xmlstream.rawDataInFn = self.rawIn
        self.xmlstream.rawDataOutFn = self.rawOut

    def rawIn(self,data):
        """data is the input stanza"""
        #print 'IN ', data
        pass

    def rawOut(self,data):
        """data is the output stanza"""
        #print 'OUT ', data
        pass

    def onDisconnected(self, xs):
        """
        xmlstream.STREAM_END_EVENT handler.
        Calls when client disconnected from server
        """
        
        pass

    def onAuthenticated(self, xs):
        """
        xmlstream.STREAM_AUTHD_EVENT handler.
        Calls when client authenticated on server.
        Setup dispatcher and any features for client
        """
        
        self.dispatcher = Dispatcher(xs, self.client_jid)
        #self.dispatcher.registerHandler((plugins.BaseCommand, self))
        plugins.register(self.dispatcher, self)
        
        self.disco = Disco(self.dispatcher)
        self.disco.init()
        
        p = Presence(status="I'm ur bot")
        self.roster = Roster(self.dispatcher, p)
        self.roster.init()
        
        self.version = ClientVersion(self.dispatcher, 
                                     "Xmppbot Prime. Optimus's brother",
                                     'v%s' % version, 'Linux')
        self.version.init(self.disco)
        
        #set handlers for roster's signals
        dispatcher.connect(self.onSubscribe, 
                           self.roster.subscribe)
        dispatcher.connect(self.onRosterGot, 
                           self.roster.roster_got)
        dispatcher.connect(self.onAvailable, 
                           self.roster.resource_available)
        dispatcher.connect(self.onUnvailable, 
                           self.roster.resource_unavailable)
        
    def onInitFailed(self, xs):
        """
        xmlstream.STREAM_INIT_FAILED_EVENT handler.
        Calls when client authenticated on server was failed.
        """
        
        pass

    #handlers for roster's signals
    
    def onAvailable(self, sender, item, presence):
        """roster.resourse_available handler."""
        pass
        
    def onUnvailable(self, sender, item, presence):
        """roster.resourse_unavailable handler."""
        pass

    def onRosterGot(self, sender):
        """roster.roster_got handler."""
        pass

    def onSubscribe(self, sender, presence):
        """roster.subscribe handler."""
        
        presence.type_ = 'subscribed'
        presence.to = presence.from_
        presence.from_ = None
        self.dispatcher.send(presence)
        presence.type_ = 'subscribe'
        self.dispatcher.send(presence)
        

version = '0.1'
configDefault = 'xmppbot.conf'

#read command-line's params
optparser = OptionParser(version="Xmpp bot version : %s"  % version)
optparser.add_option('-c', 
                     '--config', 
                     metavar='FILE', 
                     dest='configFile', 
                     help="Read config from custom file")

(options, args) = optparser.parse_args()
configFile = options.configFile

#load configuration settings
config = ConfigParser.ConfigParser()
config.read(configFile if configFile else configDefault)

jid = config.get('connect', 'jid')
host = config.get('connect', 'host')
password = config.get('connect', 'password')
port = config.get('connect', 'port')

#connection to server
cl = Client(reactor, internJID(jid), 
            host, password, port)
reactor.run()
