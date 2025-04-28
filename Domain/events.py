import uuid
from datetime import datetime
from abc import ABC, abstractmethod


class Event(ABC):
    """Base interface for all events"""

    @property
    @abstractmethod
    def id(self):
        pass

    @property
    @abstractmethod
    def timestamp(self):
        pass


class BaseEvent(Event):
    """Base implementation for all events"""

    def __init__(self):
        self._id = str(uuid.uuid4())
        self._timestamp = datetime.now().isoformat()

    @property
    def id(self):
        return self._id

    @property
    def timestamp(self):
        return self._timestamp

    def to_dict(self):
        """Convert event to dictionary for serialization"""
        return {
            'id': self.id,
            'timestamp': self.timestamp
        }

    @classmethod
    def from_dict(cls, data):
        """Create event from dictionary"""
        instance = cls()
        instance._id = data.get('id', str(uuid.uuid4()))
        instance._timestamp = data.get('timestamp', datetime.now().isoformat())
        return instance


class Type1Event(BaseEvent):
    """Event of type 1"""

    def __init__(self, data=None):
        super().__init__()
        self.data = data

    def to_dict(self):
        result = super().to_dict()
        result['data'] = self.data
        return result

    @classmethod
    def from_dict(cls, data):
        instance = super(Type1Event, cls).from_dict(data)
        instance.data = data.get('data')
        return instance


class Type2Event(BaseEvent):
    """Event of type 2"""

    def __init__(self, data=None):
        super().__init__()
        self.data = data

    def to_dict(self):
        result = super().to_dict()
        result['data'] = self.data
        return result

    @classmethod
    def from_dict(cls, data):
        instance = super(Type2Event, cls).from_dict(data)
        instance.data = data.get('data')
        return instance


class Type3Event(BaseEvent):
    """Event of type 3"""

    def __init__(self, data=None):
        super().__init__()
        self.data = data

    def to_dict(self):
        result = super().to_dict()
        result['data'] = self.data
        return result

    @classmethod
    def from_dict(cls, data):
        instance = super(Type3Event, cls).from_dict(data)
        instance.data = data.get('data')
        return instance


class Type4Event(BaseEvent):
    """Event of type 4, generated after processing Type3Event"""

    def __init__(self, data=None, source_event_id=None):
        super().__init__()
        self.data = data
        self.source_event_id = source_event_id

    def to_dict(self):
        result = super().to_dict()
        result['data'] = self.data
        result['source_event_id'] = self.source_event_id
        return result

    @classmethod
    def from_dict(cls, data):
        instance = super(Type4Event, cls).from_dict(data)
        instance.data = data.get('data')
        instance.source_event_id = data.get('source_event_id')
        return instance