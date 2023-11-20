from typing import List

from pydantic import BaseModel

from chat.room.schemas import RoomSchema


class GuestSchema(BaseModel):
    id: int
    name: str
    rooms: List[RoomSchema]

    class Config:
        from_attributes = True


class SetGuestSchema(BaseModel):
    name: str

    class Config:
        from_attributes = True
