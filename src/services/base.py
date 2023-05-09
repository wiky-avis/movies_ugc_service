from abc import ABC, abstractmethod


class BaseService(ABC):
    @abstractmethod
    async def send(self, *args):
        pass
