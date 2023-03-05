import json
import os

from watchdog.events import FileSystemEventHandler

from Common.Utils.Consts import (CREATED, DELETED, EVENT_TYPE, FILE_PATH, MOVED, RABBITMQ_QUEUE)
from Common.Utils.RabbitMQUtils import get_rabbitmq_connection


class HandleEvent(FileSystemEventHandler):
    def __init__(self, watch_folder):
        self.watch_folder = watch_folder

    def on_created(self, event):
        self.print_event(event)
        if not event.is_directory:
            self.send_message(event.src_path, CREATED)

    def on_moved(self, event):
        self.print_event(event)
        if not event.is_directory:
            self.send_message(event.dest_path, MOVED)

    def on_deleted(self, event):
        self.print_event(event)
        if not event.is_directory:
            self.send_message(event.src_path, DELETED)

    @staticmethod
    def print_event(event):
        print(f'Capture event: {event}')

    @staticmethod
    def send_message(filepath: str, event_type: str):
        # Create rabbitmq connection to send the message
        connection, channel = get_rabbitmq_connection()

        message = {
            FILE_PATH: filepath,
            EVENT_TYPE: event_type
        }

        # Publish the message to rabbitmq
        channel.basic_publish(exchange='',
                              routing_key=os.getenv(RABBITMQ_QUEUE),
                              body=json.dumps(message))

        connection.close()

        print(f'Sent message to rabbitMQ: {message}')
