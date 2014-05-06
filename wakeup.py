#!/usr/bin/env python

"""
    Get the events that match a search query from the nominated google calendar,
    and schedule a wake sequence.
    Adapted from Simple Google Calendar Alarm Clock by Bart Bania
"""
from apscheduler.scheduler import Scheduler

import gdata.calendar.service as GServ
from datetime import datetime, timedelta
from dateutil import parser
import pytz
from lib.net import wait_until_network
from presets import alarm_cycle
import settings

import logging
logging.basicConfig()

if settings.DEBUG:
    CHECK_CALENDAR_EVERY = 10 #secs
else:
    CHECK_CALENDAR_EVERY = 60*10 #secs


scheduler = Scheduler()

# set up a google calendar connection
calendar_service = GServ.CalendarService()
calendar_service.email = settings.G_LOGIN
calendar_service.password = settings.G_PASSWORD
calendar_service.source = 'RPi Alarm Clock'

local = pytz.timezone(settings.TIMEZONE)

def check_calendar():
    print 'Query for "%s" events on %s' % (settings.CALENDAR_QUERY, settings.CALENDAR_NAME)

    query = GServ.CalendarEventQuery(user=settings.CALENDAR_NAME, visibility="private", projection='full', text_query=settings.CALENDAR_QUERY)
    query.start_min = local.localize(datetime.now()).isoformat()
    query.start_max = local.localize(datetime.now() + timedelta(days=7)).isoformat()
    query.singleevents = 'true'  #  enables creation of repeating events

    feed = calendar_service.CalendarQuery(query)
    local_now = local.localize(datetime.now())

    #clear out current schedule of alarms - just in case any are deleted or changed
    try:
        scheduler.unschedule_func(do_alarm)
    except KeyError:
        pass

    for i, event in enumerate(feed.entry):
        for when in event.when:
            t = parser.parse(when.start_time) - timedelta(seconds=settings.PRE_WAKEUP_TIME)
            if t > local_now:
                print "Scheduled alarm for %s ('%s') (starting %s)" % (when.start_time, event.title.text, t)
                scheduler.add_cron_job(do_alarm, month=t.month, day=t.day, hour=t.hour, minute=t.minute, second=t.second)

def do_alarm():
    local_now = local.localize(datetime.now())
    print "%s: ALARM" % local_now

    [alarm_cycle(settings.B) for B in settings.BULBS]

    # #play a random mp3 file
    # fn = random.choice(os.listdir(settings.AUDIO_PATH))
    # print "Playing %s" % fn
    # f = os.path.join(settings.AUDIO_PATH, fn)
    #
    # player = subprocess.Popen(["mplayer", f], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    # player.stdin.write("volume 0 1\n")
    #
    # def _ramp_volume(volume):
    #     volume += 10
    #     volume = min(settings.MAX_VOLUME, volume)
    #     player.stdin.write("volume %s 1\n" % volume)
    #     if volume < settings.MAX_VOLUME:
    #         print volume
    #         t = Timer(0.5, _ramp_volume, (volume, ))
    #         t.start()
    # _ramp_volume(0)
    #
    # player.wait()

def start_calendar_scheduler():
    calendar_service.ProgrammaticLogin()

    # do_alarm()
    check_calendar()
    scheduler.add_interval_job(check_calendar, seconds=CHECK_CALENDAR_EVERY)  #  define refresh rate.
    scheduler.start()                                     #  runs the program indefinitely on an interval of x seconds


if __name__ == '__main__':
    wait_until_network()
    start_calendar_scheduler()
    while True:
        pass