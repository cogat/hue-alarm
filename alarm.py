import json
import requests
from datetime import datetime, timedelta, time

import pytz
local = pytz.timezone ("Australia/Sydney")

IP = "10.0.1.12"
USER = "gregturner"
BULB = 3

PRE_WAKEUP_TIME = 15*60 #secs to go from first light to dawn
LIE_IN_TIME = 10*60 #secs to stay at dawn before moving to daylight
DAYLIGHT_TRANSITION = 2*60 # secs to transition to daylight
DAYLIGHT_HOLD = 60*60 # secs to stay at daylight

# in n seconds after the last stage is completed, do this.
STAGES = [
    (0, {
        "on": True, # first light
        "bri": 0,
        "hue": 2048,
        "sat": 255,
        # "transitiontime": 5 #transition time in secs, unlike Philips API
    }),
    (1, {"on": True, "ct": 400, "bri": 255, "transitiontime": PRE_WAKEUP_TIME-1 }), #dawn
    (PRE_WAKEUP_TIME + LIE_IN_TIME - 1, {"on": True, "ct": 300, "bri": 255, "transitiontime": DAYLIGHT_TRANSITION }), # daylight
    (DAYLIGHT_TRANSITION + DAYLIGHT_HOLD, {
        "on": True,
        "bri": 0,
        "hue": 2048,
        "sat": 255,
        "transitiontime": 5
    }),
    (1, {"on": False }),
]


API_URL = "http://%s/api/%s" % (IP, USER)
STATE_URL = "%s/lights/%s/state" % (API_URL, BULB)
SCHEDULE_URL = "%s/schedules" % (API_URL)


def schedule(localtime, command_body):
    local_dt = local.localize(localtime)
    utc_dt = local_dt.astimezone(pytz.utc)

    data = {
        "command": {
            "address": "/api/%s/lights/%s/state" % (USER, BULB),
            "method": "PUT",
            "body": command_body,
        },
        "time": utc_dt.isoformat()[:19]
    }

    response = requests.post(SCHEDULE_URL, data=json.dumps(data))
    print response.content

def clear_schedules():
    r = requests.get(SCHEDULE_URL).json()
    for id in r.keys():
        requests.delete("%s/%s" % (SCHEDULE_URL, id))

def set_one_alarm(awaketime):
    t = awaketime - timedelta(seconds=PRE_WAKEUP_TIME) #start the transition so that the wakeup time is reached at the target time
    for t_offset, command in STAGES:
        try:
            command['transitiontime'] = int(command['transitiontime'] * 10)
        except KeyError:
            pass
        t += timedelta(seconds=t_offset)
        schedule(t, command)

def get_next_alarm_datetime(t):
    #return the next occurrence of time t.
    now = datetime.now()
    day = datetime.today()
    if now.time() >= t:
        day += timedelta(1)
    return datetime.combine(day, t)

def set_next_alarm(t):
    #set an alarm for the next occurrence of [time]
    set_one_alarm(get_next_alarm_datetime(t))

def set_ramped_alarms(num_days, origin_time, destination_time):
    day1 = get_next_alarm_datetime(origin_time)
    day2 = datetime.combine(day1.date() + timedelta(num_days - 1), destination_time)

    diff = (day2 - day1) / (num_days - 1)

    for n in range(num_days):
        d = day1 + n * diff
        print n, d
        set_one_alarm(d)


# clear_schedules()
set_next_alarm(time(5, 15   ))
# set_one_alarm(datetime.now()+timedelta(seconds=2))


# set_ramped_alarms(20, time(7,30), time(6,00))


# state = STAGES[-1][1]
# response = requests.put(STATE_URL, data=json.dumps(state))
# print STATE_URL
# print response
# print response.content