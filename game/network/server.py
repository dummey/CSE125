from network import Network
from threading import Thread
from cPickle import loads, dumps
import time, sys
import utils

class Server(object):
    def __init__(self, port=8000,
            logging=False, auto_shutdown=False,
            callbacks={}, run_local=False, **kwargs):
        self.server = Network(run_local=run_local, callbacks=callbacks, port=port)
        self.port = self.server.port
        self.clients = self.server.clients
        self.server.serve_forever()
        self.updateCounter = 0
        self.auto_shutdown = auto_shutdown
        self.callbacks = callbacks
        self.logging = logging

    def broadcastUpdate(self, tag, data):
        """Server to all clients communication. Uses sendUpdate for
        single point of communication with clients."""
        self.lastUpdateTime = time.time()
        self.updateCounter += 1
        bad = 0
        for clientId in range(0, len(self.clients)):
            if self.clients[clientId] is not None:
                self.sendUpdate(clientId, tag, data)
            else:
                bad += 1
        if bad == len(self.clients) and len(self.clients) > 1:
            self.server.shutdown()
            sys.exit()

    def sendUpdate(self, clientId, tag, data):
        """Server to a single client communication"""
        # print "sending update with tag '%s' and data %s to client %s" % (tag, data, clientId)
        try:
            if not self.clients[clientId].running:
                self.clients[clientId] = None
            self.clients[clientId].send(tag, dumps(data))
        except Exception, e:
            print "Exception!", e, type(e)
            self.clients[clientId] = None
            bad = 0
            for clientId in range(0, len(self.clients)):
                if self.clients[clientId] is None:
                    bad += 1
            if bad == len(self.clients) and len(self.clients) >= 1 and self.auto_shutdown:
                self.server.shutdown()
                sys.exit()

    def reset(self):
        """Resets state variables for the server,
        essentially 'disconnecting' clients from the server"""
        if self.logging: self.lastEventRecievedTime = []
        self.lastUpdateTime = 0
        self.clients = []
        self.events = []

    def register(self, func, tag):
        """Decorator, must include a specific tag. Takes a function that will accept three arguments
        a cliendID, a tag, and the data itself"""
        self.callbacks[tag] = func
        return func

    def shutdown(self):
        self.server.shutdown()


if __name__ == "__main__":
    server = Server(run_local=True)
