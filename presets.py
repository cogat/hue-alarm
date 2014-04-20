from libhue import set_state

PRESETS = {
    'off': {
        'on': False
    },
    'relax': {
        "on": True,
        "ct": 467,
        "transitiontime": 50
    },
    'sunrise': {
        "on": True,
        "ct": 400,
        "transitiontime": 50
    },
    'reading': {
        "on": True,
        "ct": 343,
    },
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
    set_state(light, {'on': False, 'transitiontime': int(round(seconds * 0.33 * 10)) }, delay=seconds * 0.66)
