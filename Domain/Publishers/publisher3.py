import time
import random
from datetime import datetime
from Domain.events import Type3Event
from Infrastructure.messaging import RabbitMQConnection, RabbitMQPublisher
from Domain.Publishers.publisher1 import setup_logger


def run_publisher3(connection_string="amqps://username:password@hostname/vhost"):
    """Run Type3 event publisher"""
    logger = setup_logger("Publisher3")
    logger.info("Starting Type3 Publisher")

    connection = RabbitMQConnection(connection_string, logger)
    publisher = RabbitMQPublisher(connection, Type3Event, logger)

    try:
        # Publish events at random intervals (3-15 seconds)
        while True:
            event = Type3Event(data=f"Type3 event at {datetime.now()}")
            logger.info(f"Publishing Type3Event: {event.data}")
            publisher.publish(event)

            # Random interval between 3 and 15 seconds
            delay = random.randint(3, 15)
            logger.info(f"Next Type3 event will be published in {delay} seconds")
            time.sleep(delay)
    except KeyboardInterrupt:
        logger.info("Publisher interrupted, shutting down...")
    finally:
        if connection._connection and not connection._connection.is_closed:
            connection._connection.close()
        logger.info("Publisher shut down")