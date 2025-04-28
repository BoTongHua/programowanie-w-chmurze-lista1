import time
from core.events import Type2Event
from infrastructure.messaging import RabbitMQConnection, RabbitMQConsumer
from publishers.publisher1 import setup_logger


def run_consumer2(connection_string="amqps://username:password@hostname/vhost"):
    """Run Type2 event consumer"""
    logger = setup_logger("Consumer2")
    logger.info("Starting Type2 Consumer")

    connection = RabbitMQConnection(connection_string, logger)

    def process_event(event):
        """Process Type2 event"""
        logger.info(f"Type2 Consumer processing event: {event.id}")
        time.sleep(0.7)  # Simulate processing
        logger.info(f"Type2 Consumer finished processing event: {event.id}")

    consumer = RabbitMQConsumer(connection, Type2Event, process_event, logger)

    try:
        consumer.start_consuming()
    except KeyboardInterrupt:
        logger.info("Consumer interrupted, shutting down...")
    finally:
        if connection._connection and not connection._connection.is_closed:
            connection._connection.close()
        logger.info("Consumer shut down")