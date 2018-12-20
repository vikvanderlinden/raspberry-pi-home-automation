"""
    The main file of the application.
"""
import os
from watchdog.events import PatternMatchingEventHandler #pylint: disable=E0401
from watchdog.observers import Observer #pylint: disable=E0401
# import switches
import schedule #pylint: disable=E0401
import actions #pylint: disable=E0401
import speech #pylint: disable=E0401
import database #pylint: disable=E0401
import Config #pylint: disable=E0401
from . import time


def notify(src_path):
    """
        Decodes which notification, removes notification file
        and executes proper action to notification.
    """
    file_name = src_path.split('/')[-1]
    notification = file_name.split('.')[0]
    os.remove(src_path)

    speech.say("I saw you updated the %s, i'll update my %s as well."
               % tuple([NOTIFICATIONS[notification][0]]*2))
    NOTIFICATIONS[notification][1]()


class NotificationHandler(PatternMatchingEventHandler):
    """Handles creation of server-side notifications"""
    patterns = ["*.notify"]

    def on_created(self, event):
        """Handles creation of event"""
        notify(event.src_path)

CONFIG = Config('./configuration/.env')

# Variables
LAST_AUTO_UPDATE = time.get_time()

# Initializations
DATABASE = database.DB(CONFIG.get('database.host'), CONFIG.get('database.user'),
                       CONFIG.get('database.password'), CONFIG.get('database.name'))
ACTIONS = actions.Actions(DATABASE)
SCHEDULE = schedule.Schedule(DATABASE, ACTIONS)
OBSERVER = Observer()

# Definitions
NOTIFICATIONS = {
    "update_schedule": ["schedule", SCHEDULE.update],
    "update_actions": ["actions", ACTIONS.update]
}

# Prepare system
OBSERVER.schedule(NotificationHandler(), path=CONFIG.get('notifications.path'), recursive=False)
OBSERVER.start()

if __name__ == "__main__":
    speech.say("Setting up the system")
    speech.say("Initializing")
    speech.say("Done, application starts now")

    try:
        while True:
            if time.get_time() - LAST_AUTO_UPDATE > 24 * 60 * 60:
                # Auto-refresh schedule every day
                LAST_AUTO_UPDATE = time.get_time()
                SCHEDULE.update()
                speech.say("I did an autoupdate as is was a full day ago")

            SCHEDULE.run()
            time.sleep(1)
    except KeyboardInterrupt:
        DATABASE.close_connection()
        OBSERVER.stop()

    OBSERVER.join()
