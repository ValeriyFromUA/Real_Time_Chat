from datetime import datetime

from pydantic import BaseModel, field_validator


class RoomSchema(BaseModel):
    name: str
    description: str

    class Config:
        from_attributes = True


class RoomDetailSchema(BaseModel):
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
