from abc import ABC, abstractmethod


class BaseProducer(ABC):
    @abstractmethod
    def send(self, *args, **kwargs):
        """Метод публикации события"""
        pass


class BaseConsumer(ABC):
    @abstractmethod
    def consume(self, *args, **kwargs):
        """Метод чтения события"""
        pass
