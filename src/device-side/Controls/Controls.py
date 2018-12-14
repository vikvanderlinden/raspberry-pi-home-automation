from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
from Switches import *
from Schedule import *
from Actions import *
from Speech import *
from Time import *
from DB import *
import time
import os


say("Setting up the system")

def notify(src_path):
	"""
		Decodes which notification, removes notification file and executes proper action to notification.
	"""
	file_name = src_path.split('/')[-1]
	notification = file_name.split('.')[0]
	os.remove(src_path)

	say("I saw you updated the %s, i'll update my %s as well." % tuple([notifications[notification][0]]*2))
	notifications[notification][1]()


class NotificationHandler(PatternMatchingEventHandler):
	patterns = ["*.notify"]

	def on_created(self, event):
		notify(event.src_path)


# Variables
database_host = "127.0.0.1"
database_user = "root"
database_password = "RaspberryVV"
database_database = "controls"
last_auto_update = get_time()

path_to_watch = "/var/www/html/notifications"

say("Initializing");

# Initializations
database = DB(database_host, database_user, database_password, database_database)
actions = Actions(database)
schedule = Schedule(database, actions)
observer = Observer()

# Definitions
notifications = {
					"update_schedule": ["schedule", schedule.update],
					"update_actions": ["actions", actions.update]
				}

# Prepare system
observer.schedule(NotificationHandler(), path=path_to_watch, recursive=False)
observer.start()

say("Done, application starts now");

try:
	while True:
		if get_time() - last_auto_update > 24 * 60 * 60:
			# Auto-refresh schedule every day
			last_auto_update = get_time()
			schedule.update()
			say("I did an autoupdate as is was a full day ago")

		schedule.run()
		time.sleep(1)
except KeyboardInterrupt:
	database.close_connection()
	observer.stop()

observer.join()
