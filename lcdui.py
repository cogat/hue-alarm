#!/usr/bin/python
# -*- coding: utf-8 -*-

import curses
from threading import Timer
from datetime import timedelta, datetime, time
from lib.libhue import modify_temperature, modify_brightness, set_state, toggle
from lib.net import get_ip_address
from presets import turn_off_after, show_preset
import settings

stdscr = None

try:
    from lib.Adafruit_CharLCDPlate import Adafruit_CharLCDPlate as LCD
    # Initialize the LCD plate.  Should auto-detect correct I2C bus.  If not,
    # pass '0' for early 256 MB Model B boards or '1' for all later versions
    lcd = LCD()
except ImportError:
    lcd = None

def _t(s, l):
    return unicode(s).ljust(l)[:l]

# ╔════════════════╗
# ║20:08 a06:00 10m║
# ║b100% Showers   ║
# ╚════════════════╝
BACKLIGHT_TIMER = None
def display_message(msg, colour="GREEN"):
    global stdscr
    if lcd:
        global BACKLIGHT_TIMER
        lcd.clear()
        lcd.backlight(getattr(lcd, colour))
        lcd.message(msg)
        if BACKLIGHT_TIMER and BACKLIGHT_TIMER.is_alive():
            BACKLIGHT_TIMER.cancel()
        BACKLIGHT_TIMER = Timer(2, lcd.backlight, (lcd.OFF, ))
        BACKLIGHT_TIMER.start()

    if stdscr:
        lines = msg.split("\n")[:2]
        if len(lines) < 2:
            lines.append("")
        stdscr.addstr(0, 0, "-"*18)
        for i, line in enumerate(lines):
            stdscr.addstr(i+1, 0, "|%s|" % _t(line,16))
        stdscr.addstr(3, 0, "-"*18)



class Status(object):
    def __init__(self):
        self.next_alarm = None
        self.turn_off = 0
        self.brightness = 0
        self.weather = ""

    def display(self, line1=None, line2=None, colour="GREEN"):

        if line1 is None:
            formatted_time = unicode(datetime.now().time())
            if self.turn_off:
                if self.turn_off >= 3660:
                    formatted_turn_off = "%sh" % int(round(self.turn_off/3600))
                elif self.turn_off >= 60:
                    formatted_turn_off = "%sm" % int(round(self.turn_off/60))
                else:
                    formatted_turn_off = "%ss" % int(self.turn_off)

            else:
                formatted_turn_off = ""

            line1 = "%s a%s %s" % (_t(formatted_time,5), _t(self.next_alarm.time(), 5), _t(formatted_turn_off, 3))
        if line2 is None:
            formatted_brightness = unicode(int(round(self.brightness * 100)))
            line2 = "%s%% %s" % (_t(formatted_brightness, 3), _t(self.weather, 11))

        display_message("%s\n%s" % (line1, line2), colour)

STATUS = Status()


def adjust_brightness(amount):
    b = [modify_brightness(B, amount) for B in settings.BULBS]
    STATUS.brightness = (float(sum(b))/len(b))/255.0


def adjust_temperature(amount):
    t = [modify_temperature(B, amount) for B in settings.BULBS]


TURNOFF_TIME = None


def adjust_turnoff(d):
    global TURNOFF_TIME
    [set_state(B, {'on': True }) for B in settings.BULBS]
    if settings.DEBUG:
        diff = timedelta(seconds=d)
    else:
        diff = timedelta(minutes=d)
    if TURNOFF_TIME:
        TURNOFF_TIME += diff
    else:
        TURNOFF_TIME = datetime.now() + diff

    time_to_go = (TURNOFF_TIME - datetime.now()).total_seconds()
    [turn_off_after(B, time_to_go) for B in settings.BULBS]

    STATUS.turn_off = time_to_go

    def _clear_clock():
        global TURNOFF_TIME
        TURNOFF_TIME = None
    t = Timer(time_to_go, _clear_clock)
    t.start()


def start_ui():
    global turnoff_time
    global stdscr
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    curses.curs_set(0) #invisible cursor

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

        while True:
            charcode = stdscr.getch()
            try:
                char = chr(charcode)
            except ValueError:
                char = None

            if charcode in [ord('x')]:
                [show_preset('off', B) for B in settings.BULBS]
                display_message("Bye.")
                exit()

            elif char == '1':
                [show_preset('relax', B) for B in settings.BULBS]
            elif char == '2':
                [show_preset('sunrise', B) for B in settings.BULBS]
            elif char == '3':
                [show_preset('reading', B) for B in settings.BULBS]
            elif charcode == curses.KEY_UP:
                adjust_brightness(+26)
            elif charcode == curses.KEY_DOWN:
                adjust_brightness(-26)
            elif charcode == curses.KEY_LEFT:
                adjust_temperature(-35)
            elif charcode == curses.KEY_RIGHT:
                adjust_temperature(35)
            elif charcode == 91:
                adjust_turnoff(-5)
            elif charcode == 93:
                adjust_turnoff(5)
            elif char == ' ':
                [toggle(B) for B in settings.BULBS]
            if charcode and char != '9':
                STATUS.display()

            stdscr.refresh()

    finally:
        curses.nocbreak()
        stdscr.keypad(0)
        curses.echo()
        curses.endwin()


#
#
# BUTTONS = [
#     (lcd.UP, press_up),
#     (lcd.DOWN, press_down),
#     (lcd.LEFT, press_left),
#     (lcd.RIGHT, press_right),
#     (lcd.SELECT, press_select),
# ]

# def start_ui():
#     prev = None
#     while True:
#         any_button_pressed = False
#         for b in BUTTONS:
#             if lcd.buttonPressed(b[0]):
#                 any_button_pressed = True
#                 if b is not prev:
#                     b[1]()
#                     prev = b
#         if not any_button_pressed:
#             prev = None