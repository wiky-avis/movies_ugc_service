from abc import ABC, abstractmethod


class AbstractDatabase(ABC):
    @abstractmethod
    def get(self, *args, **kwargs):
        """Получаем данные из таблицы"""
        pass
