from typing import Any

from starlette.responses import JSONResponse


class FakeUserActivityRepository:
    async def send_view_progress(self, data: dict):
        return JSONResponse(content={"result": "Ok."})

    async def insert_or_update_view_progress(self, data: dict):
        pass

    async def get_last_view_progress(self, filter_query: dict):
        return dict(
            user_id=filter_query["user_id"],
            film_id=filter_query["film_id"],
            viewed_frame=123,
        )


class FakeProducer:
    async def send(self, key, value):
        pass


class FakeUARepository:
    def __init__(self):
        self.storage = {}
        pass

    async def insert_one(self, data: dict, table_name: str):
        # data = dict(film_id=film_id, user_id=user_id, viewed_frame=viewed_frame)
        # table_name = "view_progress"

        film_id = data["film_id"]
        user_id = data["user_id"]
        viewed_frame = data["viewed_frame"]

        key = f"{film_id}:{user_id}"

        self.storage[key] = viewed_frame

    async def update_one(
        self, filter_: dict, key: str, value: Any, table_name: str
    ):
        # filter_ = dict(film_id=film_id, user_id=user_id)
        # key = "viewed_frame"
        # value = viewed_frame
        # table_name = "view_progress"

        film_id = filter_["film_id"]
        user_id = filter_["user_id"]

        key = f"{film_id}:{user_id}"

        self.storage[key] = value

    async def find_one(self, filter_: dict, table_name: str):
        # filter_ = dict(film_id=film_id, user_id=user_id)
        # table_name = "view_progress"

        film_id = filter_["film_id"]
        user_id = filter_["user_id"]

        key = f"{film_id}:{user_id}"
        value = self.storage[key]

        return dict(
            user_id=user_id,
            film_id=film_id,
            viewed_frame=value,
        )
