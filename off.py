import json
import requests
from alarm import STATE_URL

response = requests.put(STATE_URL, data=json.dumps({'on': False, "transitiontime": 30 }))
print response.status_code, response.json()[0].has_key('success')