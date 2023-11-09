from pydantic import BaseModel


class MessagesModel(BaseModel):
    id: int
    content: str
    room_id: int

    class Config:
        from_attributes = True
