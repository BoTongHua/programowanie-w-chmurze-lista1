import time
from domain.events import Type4Event
from infrastructure.messaging import RabbitMQConnection, RabbitMQConsumer
from publishers.publisher1 import setup_logger


def run_consumer4(connection_string="amqps://username:password@hostname/vhost"):
    """Run Type4 event consumer"""
    logger = setup_logger("Consumer4")
    logger.info("Starting Type4 Consumer")

    connection = RabbitMQConnection(connection_string, logger)

    def process_event(event):
        """Process Type4 event"""
        logger.info(f"Type4 Consumer processing event: {event.id}, SourceEventId: {event.source_event_id}")
        time.sleep(0.8)  # Simulate processing
        logger.info(f"Type4 Consumer finished processing event: {event.id}")

    consumer = RabbitMQConsumer(connection, Type4Event, process_event, logger)

    try:
        consumer.start_consuming()
    except KeyboardInterrupt:
        logger.info("Consumer interrupted, shutting down...")
    finally:
        if connection._connection and not connection._connection.is_closed:
            connection._connection.close()
        logger.info("Consumer shut down")