#!/usr/bin/python
import curses
from datetime import datetime, timedelta
import requests
from alarm import set_one_alarm
from hue import toggle, set_state, modify_brightness
import settings

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)

"""
Keypad:

91  32  93
27  UP  113
LT  10  RT
48  DN  127
49  50  51
52  53  54
55  56  57
"""

def display_status(text):
    y, x = stdscr.getmaxyx()
    stdscr.addstr(y-1, 5, text.ljust(x-6), curses.A_BOLD)

try:
    row = 0

    stdscr.addstr(row,5,"Hue Alarm Clock")

    row += 2
    stdscr.addstr(row,5,"Space = Toggle light")
    row += 1
    stdscr.addstr(row,5,"1     = Relax light")
    row += 1
    stdscr.addstr(row,5,"2     = Reading light")
    row += 2
    stdscr.addstr(row,5,"Up    = Brighter")
    row += 1
    stdscr.addstr(row,5,"Down  = Dimmer")
    row += 2
    stdscr.addstr(row,5,"x     = Exit")

    row += 2

    while True:
        char = stdscr.getch()
        if char == ord('1'):
            set_state(settings.BULB, {
                "on": True,
                # "bri": 224,
                "ct": 467,
                "transitiontime": 50
            })
            display_status("Relax light")
        elif char == ord('2'):
            set_state(settings.BULB, {
                "on": True,
                # "bri": 240,
                "ct": 343,
                "transitiontime": 50
            })
            display_status("Reading light")
        elif char == curses.KEY_UP:
            b = modify_brightness(settings.BULB, +26)
            display_status("Changing brightness to %s" % b)
        elif char == curses.KEY_DOWN:
            b = modify_brightness(settings.BULB, -26)
            display_status("Changing brightness to %s" % b)
        elif char == curses.KEY_RIGHT:
            display_status("Right")
        elif char == curses.KEY_LEFT:
            display_status("Left")
        elif char == 10:
            set_one_alarm(datetime.now()+timedelta(seconds=4))
        elif char == 32:
            toggle(settings.BULB)
        elif char in [ord('x')]:
            exit()
        else:
            display_status("Char: %s" % char)
        stdscr.refresh()

finally:
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
