import os
import pika

from Common.Utils.Consts import RABBITMQ_HOST, RABBITMQ_QUEUE
from Common.Utils.Decorators import retry


@retry
def get_rabbitmq_connection():
    """Get a connection to RabbitMQ server"""
    rabbitmq_host = os.getenv(RABBITMQ_HOST)
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
    channel = connection.channel()

    # Declare the queue to consume from
    channel.queue_declare(queue=os.getenv(RABBITMQ_QUEUE))

    return connection, channel
