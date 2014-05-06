#!/usr/bin/python
from threading import Timer
from datetime import timedelta, datetime
from lib.libhue import modify_temperature, modify_brightness, set_state
from lib.net import get_ip_address
from presets import turn_off_after
import settings

try:
    from lib.Adafruit_CharLCDPlate import Adafruit_CharLCDPlate as LCD
except ImportError:
    from lib.Adafruit_CharLCDPlate_Fallback import Adafruit_CharLCDPlate as LCD


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
    display_message("Brightness:\n%s" % b)

def press_down():
    b = [modify_brightness(B, -26) for B in settings.BULBS]
    display_message("Brightness:\n%s" % b)

def press_left():
    t = [modify_temperature(B, -35) for B in settings.BULBS]
    display_message("Colour temp:\n%s" % t)

def press_right():
    t = [modify_temperature(B, +35) for B in settings.BULBS]
    display_message("Colour temp:\n%s" % t)

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
    display_message("Turning off in\n%s seconds." % round(time_to_go))
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
    host_ip = get_ip_address()
    # short_ip = ".".join(host_ip.split(".")[-2:])
    display_message("Greg's Alarm\nIP: %s" % host_ip)
    prev = None
    while True:
        any_button_pressed = False
        for b in BUTTONS:
            if lcd.buttonPressed(b[0]):
                any_button_pressed = True
                if b is not prev:
                    b[1]()
                    prev = b
            if not any_button_pressed:
                prev = None