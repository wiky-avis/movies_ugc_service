from typing import Any

from starlette.responses import JSONResponse

from src.api.v1.models.view_progress import ViewProgress


class FakeUserActivityRepository:
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

            result_dict = dict(
                user_id=user_id,
                film_id=film_id,
            )
            result_dict["ts"] = "1234"

            for k, v in row.items():
                result_dict[k] = v

            return result_dict
        except KeyError:
            return None
