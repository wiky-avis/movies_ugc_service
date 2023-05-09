from abc import ABC, abstractmethod


class BaseProducer(ABC):
    @abstractmethod
    def send(self, *args):
        """Метод публикации события"""
        pass


class BaseConsumer(ABC):
    @abstractmethod
    def consume(self, *args):
        """Метод чтения события"""
        pass
