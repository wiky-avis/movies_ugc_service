from pydantic import BaseModel


class UserViewProgressDataModel(BaseModel):
    user_id: str
    film_id: str
    viewed_frame: int
    ts: str
