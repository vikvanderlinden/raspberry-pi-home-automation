import time
import os
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
from Switches import *
from Schedule import *
from Actions import *
from Speech import *
from Time import *
from DB import *


say("Setting up the system")

def notify(src_path):
    """
        Decodes which notification, removes notification file
        and executes proper action to notification.
    """
    file_name = src_path.split('/')[-1]
    notification = file_name.split('.')[0]
    os.remove(src_path)

    say("I saw you updated the %s, i'll update my %s as well."
        % tuple([NOTIFICATIONS[notification][0]]*2))
    NOTIFICATIONS[notification][1]()


class NotificationHandler(PatternMatchingEventHandler):
    """Handles creation of server-side notifications"""
    patterns = ["*.notify"]

    def on_created(self, event):
        """Handles creation of event"""
        notify(event.src_path)


# Variables
DATABASE_HOST = "127.0.0.1"
DATABASE_USER = "root"
DATABASE_PASSWORD = "RaspberryVV"
DATABASE_NAME = "controls"
LAST_AUTO_UPDATE = get_time()

PATH_TO_WATCH = "/var/www/html/NOTIFICATIONS"

say("Initializing")

# Initializations
DATABASE = DB(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
ACTIONS = Actions(DATABASE)
SCHEDULE = Schedule(DATABASE, ACTIONS)
OBSERVER = Observer()

# Definitions
NOTIFICATIONS = {
    "update_schedule": ["schedule", SCHEDULE.update],
    "update_actions": ["actions", ACTIONS.update]
}

# Prepare system
OBSERVER.schedule(NotificationHandler(), path=PATH_TO_WATCH, recursive=False)
OBSERVER.start()

say("Done, application starts now")

try:
    while True:
        if get_time() - LAST_AUTO_UPDATE > 24 * 60 * 60:
            # Auto-refresh schedule every day
            LAST_AUTO_UPDATE = get_time()
            SCHEDULE.update()
            say("I did an autoupdate as is was a full day ago")

        SCHEDULE.run()
        time.sleep(1)
except KeyboardInterrupt:
    DATABASE.close_connection()
    OBSERVER.stop()

OBSERVER.join()
