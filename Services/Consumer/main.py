import json
import os

from dotenv import load_dotenv
from HandleMessage import HandleMessage

from Common.Utils.Consts import (DB_DATABASE, DB_HOST, DB_PASSWORD, DB_USERNAME, RABBITMQ_QUEUE)
from Common.Utils.DBUtils import Database
from Common.Utils.RabbitMQUtils import get_rabbitmq_connection

load_dotenv()


class Consumer:
    def __init__(self):
        self.connection, self.channel = get_rabbitmq_connection()
        db_conn = Database(host=os.getenv(DB_HOST),
                           username=os.getenv(DB_USERNAME),
                           password=os.getenv(DB_PASSWORD),
                           database=os.getenv(DB_DATABASE))
        # Fresh start
        db_conn.delete_all_files()

        self.message_handler = HandleMessage(db_conn)

    def start(self):
        # Define callback function for handling incoming messages
        def callback(ch, method, properties, body):
            message = json.loads(body)
            self.message_handler.handle(message)

        # Start consuming from the queue
        self.channel.basic_consume(queue=os.getenv(RABBITMQ_QUEUE),
                                   on_message_callback=callback,
                                   auto_ack=True)

        print("Waiting for messages...")
        self.channel.start_consuming()


if __name__ == '__main__':
    Consumer().start()
