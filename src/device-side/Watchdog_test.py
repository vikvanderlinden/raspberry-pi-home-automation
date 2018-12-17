import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class MyHandler(PatternMatchingEventHandler):
    """Detects created notifications"""
    patterns = ["*.notify"]

    def process(self, event):
        """Mimicks processing of event"""
        print(event.src_path.split('/')[-1].split('.')[0], event.event_type)

    def on_created(self, event):
        """Callback on created file"""
        self.process(event)

NOTIFICATION_PATH = "/var/www/html/notifications"
OBSERVER = Observer()
OBSERVER.schedule(MyHandler(), path=NOTIFICATION_PATH)
OBSERVER.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    OBSERVER.stop()

OBSERVER.join()
