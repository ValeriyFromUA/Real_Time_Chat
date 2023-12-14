from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from chat.category.models import Category
from chat.database.db import get_async_session
from chat.guest.models import Guest
from chat.guest.schemas import GuestSchema
from chat.room.models import Room

from chat.room.schemas import RoomSchema, RoomDetailSchema

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)


@router.post("/create", response_model=RoomSchema)
async def create_room(room_name: str, category_id=int, description: str = "",
                      db: AsyncSession = Depends(get_async_session)):
    room = Room(name=room_name, description=description, category_id=int(category_id))
    db.add(room)
    await db.commit()
    return room


@router.post("/join/{room_id}")
async def join_room(room_id: int, guest_id: int, db: AsyncSession = Depends(get_async_session)):
    async with db as session:
        query = select(Room).where(Room.id == room_id)
        result = await session.execute(query)
        room = result.scalars().first()

        query = select(Guest).where(Guest.id == guest_id)
        result = await session.execute(query)
        guest = result.scalars().first()
    if room and guest:
        guest.rooms.clear()
        guest.rooms.append(room)
        session.add(guest)
        await session.commit()
        return {"message": f"Guest {guest.name} joined room {room.name}"}
    else:
        return {"error": "Room or guest not found"}


@router.get("/user/{guest_id}")
async def get_user_rooms(guest_id: int, db: AsyncSession = Depends(get_async_session)):
    async with db as session:
        query = select(Guest).where(Guest.id == guest_id)
        result = await session.execute(query)
        guest = result.scalars().first()

    if guest:
        return {"rooms": [{"id": room.id, "name": room.name} for room in guest.rooms]}
    else:
        return {"error": "Guest not found"}


@router.get("/all", response_model=list[RoomDetailSchema])
async def get_rooms(db: AsyncSession = Depends(get_async_session)):
    async with db as session:
        query = select(Room)
        result = await session.execute(query)

    rooms = result.scalars().all()

    return rooms


@router.get("/users/{room_id}", response_model=list[GuestSchema])
async def get_users_in_rooms(room_id: int, db: AsyncSession = Depends(get_async_session)):
    async with db as session:
        query = select(Guest).options(selectinload(Guest.rooms)).where(Guest.rooms.any(Room.id == room_id))
        result = await session.execute(query)

    guests = result.scalars().all()

    return guests
