from pydantic import BaseModel


class GuestSchema(BaseModel):
    name: str

    class Config:
        from_attributes = True
