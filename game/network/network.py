import socket, sys, select
import threading
import SocketServer
import time
from cPickle import loads, dumps, UnpicklingError
import utils

networkCallbacks = {}
networkClients = []

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global networkClients
        global networkCallbacks
        payload = ""
        print("incoming client?")
        try:
            lenStr = self.request.recv(10)
            remaining = int(lenStr)
        except:
            print "expected 10 digit length, instead got %s"%lenStr
        while remaining > 0:
            n = ""
            if remaining > 1024:
                n = self.request.recv(1024)
            else:
                n = self.request.recv(remaining)
            payload += n
            remaining -= 1024

        if loads(payload) == 'TAG:INITIALIZE:END':
            print("client connected")
            i = len(networkClients)
            newConnection = Connection(sock=self.request, client_id=i, client=False)
            networkClients.append(newConnection)
            newConnection.send("client_id", "%s"%dumps(i))
            if "new_client" in networkCallbacks:
                t = threading.Thread(target=networkCallbacks["new_client"], args=[i, "new_client", "BAD"])
                t.start()
            newConnection.recieve()
        else:
            print("bad initial payload: |%s| %s"%(payload, len(payload)))

        # def finish(self):
        #     print"finishin"
        #     pass



class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


class Connection(object):
    def __init__(self, ip="", port=0, sock=None,
            callbacks=None, client_id=-1, client=True):
        global networkCallbacks
        self.running = True
        self.client_id = client_id
        self.client = client
        self.last_time = time.time()
        self.speed = 30
        if callbacks is None:
            self.callbacks = networkCallbacks
        else:
            self.callbacks = callbacks
        # print "I am a client: %s"%client
        # print "callbacks: %s"%self.callbacks
        self.callbacks["client_id"] = self._set_id
        self.sem = threading.Semaphore(0)
        if sock is None:
            # print("ip = %s"%ip)
            # print("port = %s"%port)

            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((ip, port))
            message = dumps("TAG:INITIALIZE:END")
            self.sock.send("%010d%s"%(len(message), message))
            self.thread = threading.Thread(target=self.recieve)
            self.thread.start()
        else:
            self.sock = sock
        self.sem.release()

    #
    def _set_id(self, tag, i):
        self.client_id = int(i)

    # This sends strings damnit, don't give me objects!
    def send(self, tag=None, message="", recieve=False):
        self.sem.acquire()
        if tag is None:
            print("sending tagless message, this is a bad idea")
            self.sock.send("%010d%s"%(len(message), message))
        else:
            message = "TAG:%s:%s:END"%(tag, message)
            try:
                select.select([], [self.sock], [])
                self.sock.send("%010d%s"%(len(message), message))
                # self.sock.send("%010d%s"%(len(message), message), socket.MSG_DONTWAIT)
            except Exception, e:
                print("bad socket: %s"%e)
                if self.client:
                    sys.exit()
                else:
                    self.shutdown()
                    self.running = False
                    
        self.sem.release()

    def recieve(self):
        self.sock.setblocking(1)
        while True:
            time.sleep(1.0/60.0)
            lenStr = ""
            payload = ""
            remaining = 0
            try:
                # print "trying"
                select.select([self.sock], [], [])
                lenStr = self.sock.recv(10)
                remaining = int(lenStr)
            except:
                if lenStr == "":
                    # print("removing client #%s"%self.client_id)
                    continue
                    # return
                else:
                    print "expected 10 digit length, instead got %s"%lenStr
            while remaining > 0 and ":END" not in payload:
                n = ""
                try:
                    if remaining > 8192:
                        n = self.sock.recv(8192)
                    else:
                        n = self.sock.recv(remaining)
                except Exception, e:
                    print "exception in the main recieve %s, %s"%(e, n)
                    return
                # print "n = %s" % n.__repr__()
                # print "len(n) = %s" % len(n)
                # print "remaining = %s" % remaining
                payload += n
                # remaining -= 8192
                remaining -= len(n)

            if ":END" in payload:
                t = threading.Thread(target=self.attempt_callback, args=[payload])
                t.start()
            else:
                print"recieved garbled message: payload: %s"%payload
            
            t = time.time()
            diff = t - self.last_time
            self.last_time = t
            newspeed = 1 / diff
            self.speed = (self.speed + newspeed) / 2



    def attempt_callback(self, payload):
        if payload[:4] == "TAG:":
            i = payload[4:].find(":")

            if i != -1:
                funcName = payload[4:4+i]

                if funcName in self.callbacks:
                    data = None
                    try:
                        data = loads(payload[i+5:])
                    except UnpicklingError, e:
                        print("failed to unpickle %s"%payload[i+5:])

                    # print("incoming data type:%s"%type(data))
                    # print("%s(%s)"%(funcName, data))

                    if self.client:
                        self.callbacks[funcName](funcName, data)
                    else:
                        self.callbacks[funcName](self.client_id, funcName, data)
                else:
                    print("unlisted callback/tag %s"%funcName)
                    print("valid callbacks: %s"%self.callbacks)
            else:
                print("poorly formatted payload %s"%payload[4:])
        else:
            print("got super shitty payload: %s"%payload)

    def shutdown(self):
        self.sock.close()

class Network(object):
    # Port 0 means to select an arbitrary unused port
    def __init__(self, run_local, port=0, client=False, callbacks={}):
        global networkClients
        global networkCallbacks
        self.port = port
        self.clients = networkClients
        self.callbacks = callbacks
        networkCallbacks = callbacks
        if not client:
            try:
                self.host = utils.get_ip_address()
            except:
                self.host = "127.0.0.1"
                print("failed to get local host name")
            if run_local:
                self.host = "127.0.0.1"
            
            for i in range(100):
                try:
                    self.server = ThreadedTCPServer((self.host, self.port), ThreadedTCPRequestHandler)
                    break
                except:
                    self.port += 1
                    print("couldn't get requested port, trying %s"%(self.port+1))
            print("Server running on %s %s"%(self.host, self.port))

            # Start a thread with the server -- that thread will then start one
            # more thread for each request
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            # Exit the server thread when the main thread terminates
            self.server_thread.setDaemon(True)

    def serve_forever(self):
        self.server_thread.start()
        print "Server loop running in thread:", self.server_thread.getName()

    def shutdown(self):
        self.server.shutdown()

    # def register_function(self, func, name):
    #     self.callbacks[name] = func


if __name__ == "__main__":
    n = Network(True)
    n.serve_forever()
    ip, port = n.server.server_address
    c = Connection(ip, port)

#
# def send(ip, port, message, recieve=False):
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.connect((ip, port))
#     sock.send("%010d%s"%(len(message), message))
#     response = None
#
#     if recieve:
#         response = ""
#         remaining = int(sock.recv(10))
#         while remaining > 0:
#             n = sock.recv(1024)
#             response += n
#             remaining -= 1024
#
#     # print "Received: %s" % response
#     sock.close()
#     return response
