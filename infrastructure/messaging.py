import pika
import json
import logging
from core.publishers import Publisher
from core.consumers import Consumer


class RabbitMQConnection:
    """Manages connection to RabbitMQ"""

    def __init__(self, connection_string, logger=None):
        self.connection_string = connection_string
        self.logger = logger or logging.getLogger(__name__)
        self._connection = None

    def get_connection(self):
        """Get or create a connection to RabbitMQ"""
        if self._connection is None or self._connection.is_closed:
            parameters = pika.URLParameters(self.connection_string)
            self._connection = pika.BlockingConnection(parameters)
            self.logger.info("Connected to RabbitMQ via CloudAMQP")
        return self._connection


class RabbitMQPublisher(Publisher):
    """RabbitMQ implementation of Publisher interface"""

    def __init__(self, connection, event_class, logger=None):
        self.connection = connection
        self.event_class = event_class
        self.logger = logger or logging.getLogger(__name__)

        # Use reflection to determine the queue name based on the event class
        self.queue_name = self._get_queue_name(event_class)

        # Create a channel and declare the queue
        self.channel = self.connection.get_connection().channel()
        self.channel.queue_declare(queue=self.queue_name, durable=False)

        self.logger.info(f"Publisher created for queue: {self.queue_name}")

    @staticmethod
    def _get_queue_name(event_class):
        """Get queue name based on the event class name, removing 'Event' suffix"""
        return event_class.__name__.replace('Event', '')

    def publish(self, event):
        """Publish an event to the message broker"""
        if not isinstance(event, self.event_class):
            raise TypeError(f"Expected event of type {self.event_class.__name__}, got {type(event).__name__}")

        self.logger.info(f"Publishing {type(event).__name__} with ID: {event.id}")

        message = json.dumps(event.to_dict())
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=message
        )

        self.logger.info(f"Published {type(event).__name__} with ID: {event.id} to queue: {self.queue_name}")


class RabbitMQConsumer(Consumer):
    """RabbitMQ implementation of Consumer interface"""

    def __init__(self, connection, event_class, callback, logger=None):
        self.connection = connection
        self.event_class = event_class
        self.callback = callback
        self.logger = logger or logging.getLogger(__name__)

        # Use reflection to determine the queue name based on the event class
        self.queue_name = self._get_queue_name(event_class)

        # Create a channel and declare the queue
        self.channel = self.connection.get_connection().channel()
        self.channel.queue_declare(queue=self.queue_name, durable=False)

        self.logger.info(f"Consumer created for queue: {self.queue_name}")

    @staticmethod
    def _get_queue_name(event_class):
        """Get queue name based on the event class name, removing 'Event' suffix"""
        return event_class.__name__.replace('Event', '')

    def consume(self, event):
        """Process an event from the message broker"""
        self.logger.info(f"Consuming {type(event).__name__} with ID: {event.id}")
        self.callback(event)

    def start_consuming(self):
        """Start consuming messages from the queue"""
        self.logger.info(f"Starting to consume messages from queue: {self.queue_name}")

        def callback(ch, method, properties, body):
            """Callback function for processing received messages"""
            try:
                self.logger.info(f"Received message from queue: {self.queue_name}")
                message = json.loads(body)
                event = self.event_class.from_dict(message)
                self.consume(event)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                self.logger.error(f"Error processing message: {str(e)}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=callback,
            auto_ack=False
        )

        self.logger.info(f"Waiting for messages on queue: {self.queue_name}")
        self.channel.start_consuming()
