import logging

from src.db.base import AbstractDatabase


# from src.db.exceptions import DatabaseError
# from src.settings.database import DatabaseSettings


logger = logging.getLogger(__name__)


class ClickRepository(AbstractDatabase):
    def get(self):
        pass
