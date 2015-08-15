'''
Created on Apr 13, 2011

@author: Dummey
'''
import sys
sys.path = ["../../deps", "../../"] + sys.path


import unittest
import client
import server
import time

#game.manager = managers.Server(8000)

localClientPort = 9000
serverPort = 8000
server = server.Server(serverPort, logging=False, run_local=True)
def cb(client, tag, data):
    pass
server.register(cb, "server_recieve")

class Test(unittest.TestCase):    
    def setUp(self):
        global server
        server.reset()
        
    def tearDown(self):
        pass
    
    def createClient(self, targetPort = 8000):
        global localClientPort, serverPort
        localClientPort += 1
        myClient = client.Client(local_port=localClientPort, local_address="127.0.0.1", 
                 remote_port=serverPort, remote_address="127.0.0.1", logging=False, run_local=True)
        
        def cb(tag, data):
            pass
        myClient.register(cb, "client_recieve")
        
        return myClient
    
    def createEightClients(self):
        return [self.createClient() for i in range(0, 8)]
    
    def testConnectClients(self):
        global server
        self.createClient()
        self.assertTrue(len(server.clients) == 1)
        
    def testFailConnectSingleClient(self):
        try: 
            self.createClient(22)
            self.assertTrue(False)
        except: 
            self.assertTrue(True)
        
    #if pop from empty stack, make sure previous test shut down correctly
    def testSendDataSingleClient(self):
        global server
        mClient = self.createClient()
        mClient.send("server_recieve", "test")
        self.assertTrue(len(server.events) == 1)
    
    def testRecieveDataSingleClient(self):
        global server
        mClient = self.createClient()
        server.sendUpdate(mClient.clientID, "client_recieve", "test")
        self.assertTrue(len(mClient.dataBuffer) == 1)
    
    def testConnectMultipleClients(self):
        global server
        self.createEightClients()
        self.assertTrue(len(server.clients) == 8)
    
    def testSendDataMultipleClients(self):
        global server
        mClients = self.createEightClients()
        counter = 0
        for client in mClients:
            counter += 1
            client.send("server_recieve", "test" + str(counter))
        self.assertTrue(len(server.events) == 8)
    
    def testRecieveDataMultipleClients(self):
        global server
        mClients = self.createEightClients()
        server.broadcastUpdate("client_recieve", "test")
        server.broadcastUpdate("client_recieve", "test2")
        for client in mClients:
            self.assertTrue(len(client.dataBuffer) == 2)
            
    def testPickle(self):
        global server
        testString = "hello world"
        mClient = self.createClient()
        mClient.send("server_recieve", testString)
        self.assertTrue(server.events[0].data == testString)
        server.broadcastUpdate("client_recieve", testString)
        self.assertTrue(mClient.dataBuffer[0] == testString)
        
    def testCallbackClient(self):
        pass
    
    def testCallbackServer(self):
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()