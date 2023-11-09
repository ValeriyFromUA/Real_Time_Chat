from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from chat.database.db import get_async_session
from chat.guest.models import Guest
from chat.room.models import Room

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)


@router.post("/create_room")
async def create_room(room_name: str, description: str = "", db: AsyncSession = Depends(get_async_session)):
    room = Room(name=room_name, description=description)
    db.add(room)
    await db.commit()
    return {"room_id": room.id, "room_name": room.name, "description": room.description, "created_at": room.created_at}


@router.post("/join_room/{room_id}")
async def join_room(room_id: int, guest_id: int, db: AsyncSession = Depends(get_async_session)):
    async with db as session:
        query = select(Room).where(Room.id == room_id)
        result = await session.execute(query)
        room = result.scalars().first()

        query = select(Guest).where(Guest.id == guest_id)
        result = await session.execute(query)
        guest = result.scalars().first()
    if room and guest:
        guest.rooms.append(room)
        session.add(guest)
        await session.commit()
        return {"message": f"Guest {guest.name} joined room {room.name}"}
    else:
        return {"error": "Room or guest not found"}


@router.get("/get_rooms/{guest_id}")
async def get_rooms(guest_id: int, db: AsyncSession = Depends(get_async_session)):
    async with db as session:
        query = select(Guest).where(Guest.id == guest_id)
        result = await session.execute(query)
        guest = result.scalars().first()

    if guest:
        return {"rooms": [{"id": room.id, "name": room.name} for room in guest.rooms]}
    else:
        return {"error": "Guest not found"}
