import os
import time

from Common.Utils.Consts import FILES_FOLDER
from watchdog.observers import Observer
from dotenv import load_dotenv

from HandleEvent import HandleEvent

load_dotenv()


class Watcher:
    def __init__(self):
        self.watch_folder = os.getenv(FILES_FOLDER)

    def start(self, stop):
        event_handler = HandleEvent(self.watch_folder)

        observer = Observer()
        observer.schedule(event_handler, self.watch_folder, recursive=False)
        observer.start()

        try:
            while True:
                time.sleep(1)
                if stop():
                    break
        except KeyboardInterrupt:
            observer.stop()

        if stop():
            return
        observer.join()


if __name__ == "__main__":
    Watcher().start((lambda: False))
