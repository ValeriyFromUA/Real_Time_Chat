from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from chat.database.db import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    messages = relationship("Message", back_populates="rooms")
    category_id = Column(Integer, ForeignKey("categories.id"))
    categories = relationship("Category", back_populates="rooms")
