from os import path

IP = "10.0.1.12"
USER = "gregturner"
BULBS = [1, 3]
TIMEZONE = "Australia/Sydney"

DEBUG = True #mostly, shorten animations

if DEBUG:
    PRE_WAKEUP_TIME = 15 #secs to go from first light to dawn
    DAYLIGHT_TRANSITION = 2 # secs to transition to daylight
    LIE_IN_TIME = 10 #secs to stay at daylight
    TURN_OFF_TIME = 15 # secs to fade daylight down
else:
    PRE_WAKEUP_TIME = 15*60 #secs to go from first light to dawn
    DAYLIGHT_TRANSITION = 15*60 # secs to transition to daylight
    LIE_IN_TIME = 2*60*60 #secs to stay at daylight
    TURN_OFF_TIME = 15*60 # secs to fade daylight down

G_LOGIN = "xxx@gmail.com" # set your email here
G_PASSWORD = "xxxx"

CALENDAR_NAME = "xyz123@group.calendar.google.com" #It's the first unique part of the shareable XML URI in the calendar
CALENDAR_QUERY = "wake" # set any word you like to be sought

AUDIO_PATH = path.abspath("~/audio") # set your mp3 files path here
MAX_VOLUME = 128

WEATHER_REGION = 'ASXX0112:1'