import socket
import urllib2
import settings


def get_ip_address():
    return [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]

def wait_until_network(internet=False):
    if internet:
        ip = "74.125.228.100" #google
    else:
        ip = settings.IP

    connected = False

    print "Waiting for network connection..."

    while not connected:
        try:
            response=urllib2.urlopen('http://%s' % ip, timeout=1)
            connected = True
        except urllib2.URLError as err: pass

    print "Connected."

    return

