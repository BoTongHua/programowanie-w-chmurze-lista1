from abc import ABC, abstractmethod

class Publisher(ABC):
    """Interface for all publishers"""
    @abstractmethod
    def publish(self, event):
        """Publish an event to the message broker"""
        pass