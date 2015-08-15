from network import Network, Connection
import sys
import datetime, time
from cPickle import loads, dumps
from threading import Thread
import socket
import utils

class Client(object):
    def __init__(self, remote_port=8000, remote_address="127.0.0.1",
                 local_port=9000, local_address="127.0.0.1", run_local=False,
                 logging=False, callbacks={}, **kwargs):
        
        self.connection = Connection(ip=remote_address, 
                                    port=remote_port, 
                                    callbacks=callbacks,
                                    client_id=0)
        
        self.dataBuffer = []
        self.logging = logging
        self.callbacks = callbacks
        
    

    def send(self, tag, data):
        """Communicates the given data to the server"""
        self.connection.send(tag, dumps(data))

    def register(self, func, tag):
        """Decorator, must include a specific tag. Takes a function that will accept two arguments
        a tag, and the data itself"""
        self.callbacks[tag] = func
        return func

    def shutdown(self):
        self.connection.shutdown()
    
    
if __name__ == "__main__":
    client = Client()