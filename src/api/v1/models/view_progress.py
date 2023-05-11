from pydantic import BaseModel, StrictInt, StrictStr


class SaveViewProgressInput(BaseModel):
    user_id: StrictStr
    viewed_frame: StrictInt
