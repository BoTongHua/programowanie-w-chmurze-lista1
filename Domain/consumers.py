from abc import ABC, abstractmethod


class Consumer(ABC):
    """Interface for all Consumers"""

    @abstractmethod
    def consume(self, event):
        """Process an event from the message broker"""
        pass

    @abstractmethod
    def start_consuming(self):
        """Start consuming messages from the queue"""
        pass