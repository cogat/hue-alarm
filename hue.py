#!/usr/bin/env python
import urllib2
from lib.net import wait_until_network
from presets import show_green_ok
import settings
from lcdui import start_ui, display_message
from wakeup import start_calendar_scheduler


if __name__ == "__main__":
    display_message("waiting for\nnetwork...", "RED")
    wait_until_network(internet=True)
    [show_green_ok(B) for B in settings.BULBS]

    start_calendar_scheduler()

    start_ui()