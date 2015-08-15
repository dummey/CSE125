import urllib
import socket

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("google.com",80))
    return s.getsockname()[0]
    
def download_files():
    print "downloading hollywood.wav"
    urllib.urlretrieve ("http://static.davidism.com/cse125/hollywood.wav", "../sounds/hollywood.wav")
    print "downloading myohmy.wav"
    urllib.urlretrieve ("http://static.davidism.com/cse125/myohmy.wav", "../sounds/myohmy.wav")
    print "downloading fluffy.wav"
    urllib.urlretrieve ("http://static.davidism.com/cse125/fluffy.wav", "../sounds/fluffy.wav")
    print "download finished"
    