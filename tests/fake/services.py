import json
from typing import Any

from starlette.responses import JSONResponse

from src.api.v1.models.film_scores import FilmAvgScore, ScoreEventType
from src.api.v1.models.view_progress import ViewProgress


class FakeViewProgressRepository:
    async def send_view_progress(self, data: dict):
        return JSONResponse(content={"result": "Ok."})

    async def insert_or_update_view_progress(self, data: dict):
        pass

    async def get_last_view_progress(self, filter_query: dict):
        return ViewProgress(
            user_id=filter_query["user_id"],
            film_id=filter_query["film_id"],
            viewed_frame=123,
            ts="1234",
        )


class FakeFilmScoresRepository:
    async def send_event(self, data: dict, event_type: ScoreEventType):
        return JSONResponse(content={"result": "Ok."})

    async def set_score(self, score_data: dict):
        pass

    async def delete_score(self, score_data: dict):
        pass

    async def get_user_score(self, user_id: str, film_id: str):
        result = dict(
            user_id=user_id,
            film_id=film_id,
            score=9,
            is_deleted=False,
        )
        return JSONResponse(content=json.dumps(result))

    async def get_top_scores(self, limit: int = 10):
        result_1 = FilmAvgScore(
            film_id="fa2745c1-831b-4f7d-9c63-fb774a1d0b7f",
            avg_score=9,
            num_scores=3,
        )
        result_2 = FilmAvgScore(
            film_id="fe06ad4c-4154-4de3-826d-d1caf1d46e6f",
            avg_score=8,
            num_scores=5,
        )
        return [result_1, result_2]


class FakeProducer:
    async def send(self, key, value, topic):
        pass


class FakeUARepository:
    def __init__(self):
        self.storage = {}
        pass

    async def insert_one(self, data: dict, table_name: str):
        # data = dict(film_id=film_id, user_id=user_id, viewed_frame=viewed_frame)
        # table_name = "view_progress"

        film_id = data.pop("film_id")
        user_id = data.pop("user_id")

        row_key = f"{film_id}:{user_id}"

        row_data = dict()
        row_data[row_key] = data

        self.storage[table_name] = row_data

    async def update_one(
        self, filter_: dict, key: str, value: Any, table_name: str
    ):
        # filter_ = dict(film_id=film_id, user_id=user_id)
        # key = "viewed_frame"
        # value = viewed_frame
        # table_name = "view_progress"

        film_id = filter_["film_id"]
        user_id = filter_["user_id"]

        row_key = f"{film_id}:{user_id}"

        storage_dict = dict()
        storage_dict[key] = value

        row_data = dict()
        row_data[row_key] = storage_dict

        self.storage[table_name] = row_data

    async def upsert(self, filter_: dict, document: dict, table_name: str):
        # filter_ = dict(film_id=film_id, user_id=user_id)
        # key = "viewed_frame"
        # value = viewed_frame
        # table_name = "view_progress"

        film_id = filter_["film_id"]
        user_id = filter_["user_id"]

        row_key = f"{film_id}:{user_id}"

        row_data = dict()
        row_data[row_key] = document

        self.storage[table_name] = row_data

    async def find_one(self, filter_: dict, table_name: str):
        # filter_ = dict(film_id=film_id, user_id=user_id)
        # table_name = "view_progress"

        try:
            film_id = filter_["film_id"]
            user_id = filter_["user_id"]

            row_key = f"{film_id}:{user_id}"

            table = self.storage[table_name]
            row = table[row_key]
            print("----row", row.dict())

            result_dict = dict(user_id=user_id, film_id=film_id, ts="1234")

            for k, v in row.items():
                result_dict[k] = v

            return result_dict
        except KeyError:
            return None
