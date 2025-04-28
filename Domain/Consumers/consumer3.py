import time
from datetime import datetime
from Domain.events import Type3Event, Type4Event
from Infrastructure.messaging import RabbitMQConnection, RabbitMQPublisher, RabbitMQConsumer
from Domain.Publishers.publisher1 import setup_logger


def run_consumer3(connection_string="amqps://username:password@hostname/vhost"):
    """Run Type3 event consumer that also publishes Type4 events"""
    logger = setup_logger("Consumer3")
    logger.info("Starting Type3 Consumer")

    connection = RabbitMQConnection(connection_string, logger)
    publisher = RabbitMQPublisher(connection, Type4Event, logger)

    def process_event(event):
        """Process Type3 event and publish Type4 event"""
        logger.info(f"Type3 Consumer processing event: {event.id}")
        time.sleep(1.0)  # Simulate processing

        # After processing, publish a Type4Event
        type4_event = Type4Event(
            data=f"Type4 event generated from Type3 event: {event.id} at {datetime.now()}",
            source_event_id=event.id
        )

        logger.info(f"Type3 Consumer publishing Type4Event with SourceEventId: {event.id}")
        publisher.publish(type4_event)

        logger.info(f"Type3 Consumer finished processing event: {event.id}")

    consumer = RabbitMQConsumer(connection, Type3Event, process_event, logger)

    try:
        consumer.start_consuming()
    except KeyboardInterrupt:
        logger.info("Consumer interrupted, shutting down...")
    finally:
        if connection._connection and not connection._connection.is_closed:
            connection._connection.close()
        logger.info("Consumer shut down")