import time
import random
from datetime import datetime
from domain.events import Type2Event
from infrastructure.messaging import RabbitMQConnection, RabbitMQPublisher
from publishers.publisher1 import setup_logger


def run_publisher2(connection_string="amqps://username:password@hostname/vhost"):
    """Run Type2 event publisher"""
    logger = setup_logger("Publisher2")
    logger.info("Starting Type2 Publisher")

    connection = RabbitMQConnection(connection_string, logger)
    publisher = RabbitMQPublisher(connection, Type2Event, logger)

    try:
        # Publish events at random intervals (2-10 seconds)
        while True:
            event = Type2Event(data=f"Type2 event at {datetime.now()}")
            logger.info(f"Publishing Type2Event: {event.data}")
            publisher.publish(event)

            # Random interval between 2 and 10 seconds
            delay = random.randint(2, 10)
            logger.info(f"Next Type2 event will be published in {delay} seconds")
            time.sleep(delay)
    except KeyboardInterrupt:
        logger.info("Publisher interrupted, shutting down...")
    finally:
        if connection._connection and not connection._connection.is_closed:
            connection._connection.close()
        logger.info("Publisher shut down")
