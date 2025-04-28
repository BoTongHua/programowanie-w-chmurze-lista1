import time
from domain.events import Type1Event
from infrastructure.messaging import RabbitMQConnection, RabbitMQConsumer
from publishers.publisher1 import setup_logger


def run_consumer1(instance_id="1", connection_string="amqps://username:password@hostname/vhost"):
    """Run Type1 event consumer"""
    logger = setup_logger(f"Consumer1-{instance_id}")
    logger.info(f"Starting Type1 Consumer (Instance {instance_id})")

    connection = RabbitMQConnection(connection_string, logger)

    def process_event(event):
        """Process Type1 event"""
        logger.info(f"Type1 Consumer (Instance {instance_id}) processing event: {event.id}")
        time.sleep(0.5)  # Simulate processing
        logger.info(f"Type1 Consumer (Instance {instance_id}) finished processing event: {event.id}")

    consumer = RabbitMQConsumer(connection, Type1Event, process_event, logger)

    try:
        consumer.start_consuming()
    except KeyboardInterrupt:
        logger.info("Consumer interrupted, shutting down...")
    finally:
        if connection._connection and not connection._connection.is_closed:
            connection._connection.close()
        logger.info("Consumer shut down")