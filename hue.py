#!/usr/bin/env python
from lib.net import wait_until_network, get_ip_address
from lcdui import start_ui, display_message
from wakeup import start_calendar_scheduler


if __name__ == "__main__":
    display_message("waiting for\nnetwork...", "RED")
    wait_until_network(internet=True)
    host_ip = get_ip_address()
    display_message("connected:\n%s" % host_ip, "VIOLET")

    start_calendar_scheduler()
    start_ui()