#!/usr/bin/python
from threading import Timer
from datetime import timedelta, datetime
from lib.libhue import modify_temperature, modify_brightness, set_state
from presets import turn_off_after
import settings

try:
    from lib.Adafruit_CharLCDPlate import Adafruit_CharLCDPlate as LCD
except ImportError:
    from lib.Adafruit_CharLCDPlate_Fallback import Adafruit_CharLCDPlate as LCD

import socket

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)

# Initialize the LCD plate.  Should auto-detect correct I2C bus.  If not,
# pass '0' for early 256 MB Model B boards or '1' for all later versions
lcd = LCD()

BACKLIGHT_TIMER = None

def display_message(msg, colour=lcd.GREEN):
    global BACKLIGHT_TIMER
    lcd.clear()
    lcd.backlight(colour)
    lcd.message(msg)
    if BACKLIGHT_TIMER and BACKLIGHT_TIMER.is_alive():
        BACKLIGHT_TIMER.cancel()
    BACKLIGHT_TIMER = Timer(2, lcd.backlight, (lcd.OFF, ))
    BACKLIGHT_TIMER.start()

def press_up():
    b = [modify_brightness(B, +26) for B in settings.BULBS]
    display_message("Brightness: %s" % b)

def press_down():
    b = [modify_brightness(B, -26) for B in settings.BULBS]
    display_message("Brightness: %s" % b)

def press_left():
    t = [modify_temperature(B, -35) for B in settings.BULBS]
    display_message("Changing temp\nto %s" % t)

def press_right():
    t = [modify_temperature(B, +35) for B in settings.BULBS]
    display_message("Changing temp\nto %s" % t)

TURNOFF_TIME = None

def press_select():
    global TURNOFF_TIME
    [set_state(B, {'on': True }) for B in settings.BULBS]
    if settings.DEBUG:
        diff = timedelta(seconds=10)
    else:
        diff = timedelta(minutes=10)
    if TURNOFF_TIME:
        TURNOFF_TIME += diff
    else:
        TURNOFF_TIME = datetime.now() + diff

    time_to_go = (TURNOFF_TIME - datetime.now()).total_seconds()
    [turn_off_after(B, time_to_go) for B in settings.BULBS]
    display_message("Turning off in %s seconds." % round(time_to_go))
    def _clear_clock():
        global TURNOFF_TIME
        TURNOFF_TIME = None
    t = Timer(time_to_go, _clear_clock)
    t.start()


BUTTONS = [
    (lcd.UP, press_up),
    (lcd.DOWN, press_down),
    (lcd.LEFT, press_left),
    (lcd.RIGHT, press_right),
    (lcd.SELECT, press_select),
]
def start_ui():
    short_ip = ".".join(host_ip.split(".")[-2:])
    display_message("Greg's Alarm\nIP: -%s" % short_ip)
    while True:
        for b in BUTTONS:
            if lcd.buttonPressed(b[0]):
                b[1]()