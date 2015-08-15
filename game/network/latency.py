'''
Created on Apr 18, 2011

@author: Dummey
'''
import unittest
import client
import server
import time

def test_callback(*args):
    # print("recieved %s %s"%(client_id, tag))
    pass


class Test(unittest.TestCase):
    localClientPort = 9000
    serverPort = 8000
    
    serverCallbacks = {"test":test_callback}

    def setUp(self):
        print "in setup"
        Test.localClientPort += 1
        Test.server = server.Server(Test.serverPort, callbacks={"test":test_callback}, run_local=True)
        Test.serverPort = Test.server.port
            

    def tearDown(self):
        Test.server.shutdown()

    def testLatencyClientToServerSmall(self):
        print "ports: %s %s"%(Test.localClientPort, Test.serverPort)

        self.client = client.Client(
            local_port=Test.localClientPort,
            local_address="127.0.0.1",
            remote_port=Test.serverPort,
            remote_address="127.0.0.1",
            run_local=True)

        testCount = 10
        testData = "test"
        startTime = time.time()

        for counter in range(0, testCount):
            #startTimes.append(time.time())
            self.client.send("test", testData)

        latency = time.time() - startTime
        print "Latency to Server small - Test Count: " + str(testCount)
        print "Avg: " + str(latency/10.0)

        self.assertTrue((latency/10.0) < 0.01)
        self.client.shutdown()
    # 
    # def testLatencyServerToClientSmall(self):
    #     print "ports: %s %s"%(Test.localClientPort, Test.serverPort)
    #     clients = []
    #     for i in range(4):
    #         clients.append(client.Client(
    #             local_port=Test.localClientPort,
    #             local_address="127.0.0.1",
    #             remote_port=Test.serverPort,
    #             remote_address="127.0.0.1",
    #             run_local=True,
    #             callbacks={"test":test_callback}))
    # 
    #     testCount = 10
    #     testData = "test"
    #     startTime = time.time()
    # 
    #     for counter in range(0, testCount):
    #         #startTimes.append(time.time())
    #         Test.server.broadcastUpdate("test", testData)
    # 
    #     latency = time.time() - startTime
    #     print "Latency to Server small - Test Count: " + str(testCount)
    #     print "Avg: " + str(latency/10.0)
    # 
    #     self.assertTrue((latency/10.0) < 0.01)
    #     
    #     for c in clients:
    #         c.shutdown()
    
    
    
    def testLatencyClientToServerLarge(self):
        print "ports: %s %s"%(Test.localClientPort, Test.serverPort)
        
        self.client = client.Client(
            local_port=Test.localClientPort,
            local_address="127.0.0.1",
            remote_port=Test.serverPort,
            remote_address="127.0.0.1",
            run_local=True)


        testCount = 10
        testData = "test" * 100000
        startTime = time.time()

        for counter in range(0, testCount):
            #startTimes.append(time.time())
            # print("test %s"%counter)
            
            self.client.send("test", testData)

        latency = time.time() - startTime
        print "Latency to Server large - Test Count: " + str(testCount)
        print "Avg: " + str(latency/10.0)

        self.assertTrue((latency/10.0) < 0.1)
        self.client.shutdown()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()