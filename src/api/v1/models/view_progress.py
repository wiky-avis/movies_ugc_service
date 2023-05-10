from pydantic import BaseModel


class SaveViewProgressInput(BaseModel):
    user_id: str
    viewed_frame: int
