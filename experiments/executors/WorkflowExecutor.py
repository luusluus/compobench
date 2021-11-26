from abc import ABC, abstractmethod
class WorkflowExecutor(ABC):
    def __init__(self, payload):
        self._payload = payload

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, value):
        self._payload = value

    @abstractmethod
    def start(self):
        pass