import json
import requests
import sys
import settings


API_URL = "http://%s/api/%s" % (settings.IP, settings.USER)
LIGHT_URL = "%s/lights/%%s/" % API_URL


def request(method, url, data=None):
    if data:
        response = method(url, data=json.dumps(data))
    else:
        response = method(url)

    if response.status_code != 200:
        sys.stderr.write("%s: %s\n" % (response.status_code, response.content))

    j = response.json()

    try:
        if j[0].has_key("error"):
            sys.stderr.write("%s:\n%s\n%s\n" % (response.status_code, response.request, response.content))
    except KeyError:
        pass

    return j


def set_state(light, state):
    request(requests.put, "%sstate" % (LIGHT_URL % light), state)


def toggle(light):
    """
    Turn light n on or off.
    """

    status = request(requests.get, LIGHT_URL % light)

    if status['state']['on']:
        set_state(light, {"on": False})
    else:
        set_state(light, {"on": True})


def modify_brightness(light, amount):
    status = request(requests.get, LIGHT_URL % light)
    b1 = status['state']['bri']
    b2 = min(b1 + amount, 255)

    if (b1 >= 0) and (b2 < 0):
        set_state(light, {"on": False, "bri": 0})
        b2 = -1
    else:
        set_state(light, {"on": True, "bri": b2})

    return b2