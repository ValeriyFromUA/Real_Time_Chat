from datetime import datetime
from typing import List, Type, Any

from pydantic import BaseModel, field_validator

from chat.room.schemas import RoomSchema


class CategorySchema(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime

    @field_validator("created_at")
    def validate_created_at(cls, value: datetime, values, **kwargs) -> str:
        if value > datetime.now():
            raise ValueError("Created date cannot be in the future.")

        formatted_date = value.strftime("%H:%M %d.%m.%Y")
        return formatted_date

    class Config:
        from_attributes = True


class CategoryRoomSchema(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    rooms: List[RoomSchema]

    @field_validator("created_at")
    def validate_created_at(cls, value: datetime, values, **kwargs) -> str:
        if value > datetime.now():
            raise ValueError("Created date cannot be in the future.")

        formatted_date = value.strftime("%H:%M %d.%m.%Y")
        print(formatted_date)
        return formatted_date

    class Config:
        from_attributes = True
        extra = 'allow'


class CategoryUpdateSchema(BaseModel):
    name: str
    description: str

    class Config:
        from_attributes = True
