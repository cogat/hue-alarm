#!/usr/bin/env python
import urllib2
from presets import show_green_ok
import settings
from ui import start_ui


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

if __name__ == "__main__":
    wait_until_network()
    show_green_ok(settings.BULB)
    start_ui()