from sqlalchemy import Column, Integer, String, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from chat.database.db import Base


class GuestMessage(Base):
    __tablename__ = "guest_messages"
    __table_args__ = (PrimaryKeyConstraint("guests_id", "messages_id"),)
    guests_id = Column(
        Integer, ForeignKey("guests.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    messages_id = Column(
        Integer, ForeignKey("messages.id", onupdate="CASCADE", ondelete="CASCADE")
    )


class GuestRooms(Base):
    __tablename__ = "guest_rooms"
    __table_args__ = (PrimaryKeyConstraint("guests_id", "rooms_id"),)
    guests_id = Column(
        Integer, ForeignKey("guests.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    rooms_id = Column(
        Integer, ForeignKey("rooms.id", onupdate="CASCADE", ondelete="CASCADE")
    )


class Guest(Base):
    __tablename__ = "guests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=False)
    messages = relationship("Message", secondary="guest_messages", backref="guests", cascade="all,delete",
                            lazy='subquery')
    rooms = relationship("Room", secondary="guest_rooms", backref="guests", cascade="all,delete", lazy='subquery')
    guest_uuid = Column(String, unique=True)
