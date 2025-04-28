import time
import logging
from datetime import datetime
from Domain.events import Type1Event
from Infrastructure.messaging import RabbitMQConnection, RabbitMQPublisher


def setup_logger(name):
    """Setup logger with console handler"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger


def run_publisher1(instance_id="1", connection_string="amqps://username:password@hostname/vhost"):
    """Run Type1 event publisher"""
    logger = setup_logger(f"Publisher1-{instance_id}")
    logger.info(f"Starting Type1 Publisher (Instance {instance_id})")

    connection = RabbitMQConnection(connection_string, logger)
    publisher = RabbitMQPublisher(connection, Type1Event, logger)

    try:
        # Publish events at regular intervals (5 seconds)
        while True:
            event = Type1Event(data=f"Type1 event from instance {instance_id} at {datetime.now()}")
            logger.info(f"Publishing Type1Event: {event.data}")
            publisher.publish(event)
            time.sleep(5)  # Fixed interval for Type1 Publishers
    except KeyboardInterrupt:
        logger.info("Publisher interrupted, shutting down...")
    finally:
        if connection._connection and not connection._connection.is_closed:
            connection._connection.close()
        logger.info("Publisher shut down")