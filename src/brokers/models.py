from pydantic import BaseModel


class UserViewProgressEventModel(BaseModel):
    user_id: str
    film_id: str
    viewed_frame: int
    event_time: str
