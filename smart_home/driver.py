from abc import ABC, abstractmethod


class Driver(ABC):
    @abstractmethod
    def detect(self):
        return True

    @abstractmethod
    def connect(self):
        return True

    @abstractmethod
    def close(self):
        return True

    @abstractmethod
    def set(self):
        return True

    @abstractmethod
    def get(self):
        return True
