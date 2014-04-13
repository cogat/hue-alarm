#!/usr/bin/python
import curses
from datetime import datetime, timedelta
import requests
from alarm import set_one_alarm

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

try:
    stdscr.addstr(0,5,"Hue Alarm Clock")

    while True:
        char = stdscr.getch()
        if char == curses.KEY_UP:
            stdscr.addstr(2,5, "Up        ")
        elif char == curses.KEY_RIGHT:
            stdscr.addstr(2,5, "Right     ")
        elif char == curses.KEY_DOWN:
            stdscr.addstr(2,5, "Down      ")
        elif char == curses.KEY_LEFT:
            stdscr.addstr(2,5, "Left      ")
        elif char == 10:
            set_one_alarm(datetime.now()+timedelta(seconds=4))
        elif char in [ord('x')]:
            exit()
        else:
            stdscr.addstr(2,5, "Char: %s" % str(char))
        stdscr.refresh()

finally:
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
