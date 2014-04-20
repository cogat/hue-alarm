
import curses
from datetime import datetime, timedelta
from threading import Timer
from libhue import toggle, set_state, modify_brightness, modify_temperature
from presets import *
import settings

turnoff_time = None

def draw_menu(stdscr, col, row):
        stdscr.addstr(row,col,"Hue Control")
        row += 2
        stdscr.addstr(row,col,"           Keys:")
        row += 2
        stdscr.addstr(row,col,"                  1 = Relax light")
        row += 1
        stdscr.addstr(row,col,"                  2 = Sunrise light")
        row += 1
        stdscr.addstr(row,col,"                  3 = Reading light")
        row += 2
        stdscr.addstr(row,col,"          ] (Vol +) = Brighter")
        row += 1
        stdscr.addstr(row,col,"          [ (Vol -) = Dimmer")
        row += 1
        stdscr.addstr(row,col,"              Left  = Cooler")
        row += 1
        stdscr.addstr(row,col,"              Right = Warmer")
        row += 2
        stdscr.addstr(row,col,"            0 (10+) = Turn off in +10 minutes")
        row += 1
        stdscr.addstr(row,col," Space (play/pause) = Toggle light on/off")
        row += 2
        stdscr.addstr(row,col,"                  x = Exit")
        row += 2


def start_ui():
    global turnoff_time

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


    def _display_status(text):
        y, x = stdscr.getmaxyx()
        stdscr.addstr(y-1, 5, text.ljust(x-6), curses.A_BOLD)


    try:

        draw_menu(stdscr, 5, 1)

        while True:
            charcode = stdscr.getch()
            try:
                char = chr(charcode)
            except ValueError:
                char = None

            if char == '1':
                show_preset('relax', settings.BULB)
                _display_status("Relax light")
            elif char == '2':
                show_preset('sunrise', settings.BULB)
                _display_status("Sunrise light")
            elif char == '3':
                show_preset('reading', settings.BULB)
                _display_status("Reading light")
            elif charcode == 91:
                b = modify_brightness(settings.BULB, -26)
                _display_status("Changing brightness to %s" % b)
            elif charcode == 93:
                b = modify_brightness(settings.BULB, +26)
                _display_status("Changing brightness to %s" % b)
            elif charcode == curses.KEY_LEFT:
                t = modify_temperature(settings.BULB, -35)
                _display_status("Changing temperature to %s" % t)
            elif charcode == curses.KEY_RIGHT:
                t = modify_temperature(settings.BULB, +35)
                _display_status("Changing temperature to %s" % t)
            elif char == '0':
                set_state(settings.BULB, {'on': True })
                if settings.DEBUG:
                    diff = timedelta(seconds=10)
                else:
                    diff = timedelta(minutes=10)
                if turnoff_time:
                    turnoff_time += diff
                else:
                    turnoff_time = datetime.now() + diff

                time_to_go = (turnoff_time - datetime.now()).total_seconds()
                turn_off_after(settings.BULB, time_to_go)
                _display_status("Turning off in %s minutes." % round(time_to_go))
                def _clear_clock():
                    global turnoff_time
                    turnoff_time = None
                t = Timer(time_to_go, _clear_clock)
                t.start()
            elif char == ' ':
                toggle(settings.BULB)
                _display_status("Toggle light")
            elif charcode in [ord('x')]:
                show_preset('off', settings.BULB)
                exit()
            else:
                _display_status("Char: %s" % charcode)
            stdscr.refresh()

    finally:
        curses.nocbreak()
        stdscr.keypad(0)
        curses.echo()
        curses.endwin()
