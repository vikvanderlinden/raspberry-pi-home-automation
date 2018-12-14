import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.notify"]

    def process(self, event):
        print(event.src_path.split('/')[-1].split('.')[0], event.event_type)

    def on_created(self, event):
        self.process(event)

arg = "/var/www/html/notifications"
observer = Observer()
observer.schedule(MyHandler(), path=arg)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
