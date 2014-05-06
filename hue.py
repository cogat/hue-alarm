#!/usr/bin/env python
import urllib2
from lib.net import wait_until_network
from presets import show_green_ok
import settings
from lcdui import start_ui
from wakeup import start_calendar_scheduler


if __name__ == "__main__":
    wait_until_network()
    [show_green_ok(B) for B in settings.BULBS]

    start_calendar_scheduler()

    start_ui()