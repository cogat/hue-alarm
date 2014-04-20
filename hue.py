#!/usr/bin/env python
import urllib2
from libhue import set_state, get_state
import settings


def wait_until_network(internet=False):
    if internet:
        ip = "74.125.228.100" #google
    else:
        ip = settings.IP

    connected = False

    print "Waiting for network connection..."

    while not connected:
        try:
            response=urllib2.urlopen('http://%s' % ip,timeout=1)
            connected = True
        except urllib2.URLError as err: pass

    print "Connected."
    return

def show_green_ok():
    """
    Show an "OK" green, and then turn off.
    """

    # print get_state(3)

    set_state(settings.BULB, {'on': True, 'bri': 1,  'hue': 15017, 'sat': 138}) #warm white
    set_state(settings.BULB, {'on': False, 'bri': 1,  'hue': 25718, 'sat': 255, 'transitiontime': 10}) #green then off

    # set_state(settings.BULB, {'on': False, 'transitiontime': 1})

if __name__ == "__main__":
    wait_until_network()
    show_green_ok()
    # start_ui()