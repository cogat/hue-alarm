from datetime import time
from alarm import clear_schedules, set_ramped_alarms

clear_schedules()
# set_next_alarm(time(5, 15   ))
# set_one_alarm(datetime.now()+timedelta(seconds=4))


set_ramped_alarms(15, time(7,20), time(6,00))
