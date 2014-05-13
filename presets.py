from lib.libhue import set_state
import settings

PRESETS = {
    'off': {
        'on': False
    },
    'relax': {
        "on": True,
        "ct": 467,
    },
    'sunrise': {
        "on": True,
        "ct": 400,
    },
    'reading': {
        "on": True,
        "ct": 343,
    },
    'first_light': {
        "on": True, # first light
        "bri": 0,
        "hue": 2048,
        "sat": 255,
        # "transitiontime": 5 #transition time in secs, unlike Philips API
    },
    'dawn': {
        "on": True,
        "ct": 400,
        "bri": 255
    },
    'daylight': {
        "on": True,
        "ct": 300,
        "bri": 255
    }
}


def show_green_ok(bulb):
    """
    Show an "OK" green, and then turn off.
    """
    set_state(bulb, {'on': True, 'bri': 1, 'hue': 25718, 'sat': 255}) #green
    set_state(bulb, {'on': False, 'bri': 1, 'hue': 15017, 'sat': 138, 'transitiontime': 5}, delay=0.5) #warm white then off


def show_preset(name, bulb):
    preset = PRESETS.get(name)
    preset.update({"transitiontime": 50})

    set_state(bulb, preset)


def turn_off_after(light, seconds):
    # do nothing for seconds * 0.66
    # fade down in seconds * 0.33
    # turn off.
    seconds = max(0, seconds)
    set_state(light, {'on': False, 'transitiontime': int(round(seconds * 0.33 * 10)) }, delay=seconds * 0.66)


def alarm_cycle(bulb):
    first_light = PRESETS.get("first_light")
    dawn = PRESETS.get("dawn")
    daylight = PRESETS.get("daylight")

    set_state(bulb, first_light)
    dawn.update({'transitiontime': int(settings.PRE_WAKEUP_TIME * 10) })
    set_state(bulb, dawn)
    daylight.update({'transitiontime': int(settings.DAYLIGHT_TRANSITION * 10)})
    set_state(bulb, daylight, delay=settings.PRE_WAKEUP_TIME)
    #wait for lie-in, then turn off
    set_state(
        bulb,
        {'on': False, 'transitiontime': settings.TURN_OFF_TIME * 10},
        delay=settings.PRE_WAKEUP_TIME + settings.DAYLIGHT_TRANSITION + settings.LIE_IN_TIME
    )
