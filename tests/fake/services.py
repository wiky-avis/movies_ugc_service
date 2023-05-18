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
