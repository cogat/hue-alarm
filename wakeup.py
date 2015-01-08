#!/usr/bin/env python

"""
    Get the events that match a search query from the nominated google calendar,
    and schedule a wake sequence.
    Adapted from Simple Google Calendar Alarm Clock by Bart Bania
"""
from pprint import pprint
from apscheduler.scheduler import Scheduler

from datetime import datetime, timedelta
from dateutil import parser
import httplib2
from oauth2client.file import Storage
import pytz
from lcdui import STATUS
from lib.net import wait_until_network
from presets import alarm_cycle
import settings

import logging
logging.basicConfig()

local = pytz.timezone(settings.TIMEZONE)

if settings.DEBUG:
    CHECK_CALENDAR_EVERY = 60 #secs
else:
    CHECK_CALENDAR_EVERY = 60*10 #secs


scheduler = Scheduler()

# set up a google calendar connection
from apiclient.discovery import build

from oauth2client import client


def establish_service():
    flow = client.flow_from_clientsecrets(
        'client_secrets.json',
        scope='https://www.googleapis.com/auth/calendar.readonly',
        redirect_uri='urn:ietf:wg:oauth:2.0:oob')

    storage = Storage('credentials.json')

    credentials = storage.get()

    if not credentials:
        auth_uri = flow.step1_get_authorize_url()
        import webbrowser
        webbrowser.open_new(auth_uri)

        auth_code = raw_input('Enter the auth code: ')
        credentials = flow.step2_exchange(auth_code)
        storage.put(credentials)

    http_auth = credentials.authorize(httplib2.Http())

    return build('calendar', 'v3', http_auth)

service = establish_service()

def check_calendar():
    print 'Query for "%s" events on %s' % (settings.CALENDAR_QUERY, settings.CALENDAR_NAME)

    request = service.events().list(
        calendarId=settings.CALENDAR_NAME,
        q=settings.CALENDAR_QUERY,
        timeMax = local.localize(datetime.now() + timedelta(days=7)).isoformat(),
        timeMin = local.localize(datetime.now()).isoformat(),
        singleEvents=True)
    response = request.execute()

    #clear out current schedule of alarms - just in case any are deleted or changed
    try:
        scheduler.unschedule_func(do_alarm)
    except KeyError:
        pass

    local_now = local.localize(datetime.now())

    for event in response['items']:
        parse_when = parser.parse(event['start']['dateTime'])
        t = parse_when - timedelta(seconds=settings.PRE_WAKEUP_TIME)
        if t > local_now:
            if (STATUS.next_alarm is None) or (parse_when < STATUS.next_alarm):
                STATUS.next_alarm = parse_when
            print "%s: Scheduled alarm for %s ('%s') (starting %s)" % (datetime.now(), event['start']['dateTime'], event['summary'], t)
            scheduler.add_cron_job(do_alarm, month=t.month, day=t.day, hour=t.hour, minute=t.minute, second=t.second)

def do_alarm():
    STATUS.next_alarm = None
    # local_now = local.localize(datetime.now())
    # print "%s: ALARM" % local_now

    [alarm_cycle(B) for B in settings.BULBS]

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
    check_calendar()
    scheduler.add_interval_job(check_calendar, seconds=CHECK_CALENDAR_EVERY)  #  define refresh rate.
    scheduler.start()  #  runs the program indefinitely on an interval of x seconds


if __name__ == '__main__':
    wait_until_network()
    start_calendar_scheduler()
    while True:
        pass

