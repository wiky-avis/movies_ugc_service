from enum import Enum

from pydantic import BaseSettings


class DBCollections(str, Enum):
    LIKES = "likes"
    REVIEWS = "reviews"  # На будущее, если понадобится
    BOOKMARKS = "bookmarks"  # На будущее, если понадобится


class BaseDBResearchSettings(BaseSettings):
    results_file_name: str = "results.csv"
    db_url: str = "mongodb://root:example@localhost:27017/"
    db_name: str = "test_database"
    n_films: int = 10000
    n_users: int = 1000000
    n_likes_min: int = 0
    n_likes_max: int = 20
    user_id_fn: str = r"user_ids"
    film_id_fn: str = r"film_ids"


research_settings = BaseDBResearchSettings()
