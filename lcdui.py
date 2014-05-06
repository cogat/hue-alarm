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

def display_message(msg, colour=lcd.GREEN):
    lcd.clear()
    lcd.backlight(colour)
    lcd.message(msg)
    t = Timer(2, lcd.backlight, (lcd.OFF, ))
    t.start()

def press_up():
    b = [modify_brightness(B, +26) for B in settings.BULBS]
    display_message("Changing brightness to %s" % b)

def press_down():
    b = [modify_brightness(B, -26) for B in settings.BULBS]
    display_message("Changing brightness to %s" % b)

def press_left():
    t = [modify_temperature(B, -35) for B in settings.BULBS]
    display_message("Changing temp\nto %s" % t)

def press_right():
    t = [modify_temperature(B, +35) for B in settings.BULBS]
    display_message("Changing temp\nto %s" % t)

turnoff_time = None

def press_select():
    [set_state(B, {'on': True }) for B in settings.BULBS]
    if settings.DEBUG:
        diff = timedelta(seconds=10)
    else:
        diff = timedelta(minutes=10)
    if turnoff_time:
        turnoff_time += diff
    else:
        turnoff_time = datetime.now() + diff

    time_to_go = (turnoff_time - datetime.now()).total_seconds()
    [turn_off_after(B, time_to_go) for B in settings.BULBS]
    display_message("Turning off in %s seconds." % round(time_to_go))
    def _clear_clock():
        global turnoff_time
        turnoff_time = None
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
    display_message("Greg's Alarm\nip: ...%s" % short_ip)
    while True:
        for b in BUTTONS:
            if lcd.buttonPressed(b[0]):
                b[1]()

    #
    #
    # Cycle through backlight colors
    # col = (lcd.RED , lcd.YELLOW, lcd.GREEN, lcd.TEAL,
    #        lcd.BLUE, lcd.VIOLET, lcd.ON   , lcd.OFF)
    # for c in col:
    #     lcd.backlight(c)
    #     sleep(.5)
    #
    # # Poll buttons, display message & set backlight accordingly
    # btn = ((lcd.LEFT  , 'Red Red Wine'              , lcd.RED),
    #        (lcd.UP    , 'Sita sings\nthe blues'     , lcd.BLUE),
    #        (lcd.DOWN  , 'I see fields\nof green'    , lcd.GREEN),
    #        (lcd.RIGHT , 'Purple mountain\nmajesties', lcd.VIOLET),
    #        (lcd.SELECT, 'Bo Selecta'                , lcd.YELLOW))
    # prev = -1
    # while True:
    #     for b in btn:
    #         if lcd.buttonPressed(b[0]):
    #             if b is not prev:
    #                 lcd.clear()
    #                 lcd.message(b[1])
    #                 lcd.backlight(b[2])
    #                 prev = b
    #             break
