from abc import ABC, abstractmethod


class BaseRepository(ABC):
    @abstractmethod
    async def insert_one(self, *args, **kwargs):
        pass

    @abstractmethod
    async def update_one(self, *args, **kwargs):
        pass

    @abstractmethod
    async def upsert(self, *args, **kwargs):
        pass

    @abstractmethod
    async def find_one(self, *args, **kwargs):
        pass
