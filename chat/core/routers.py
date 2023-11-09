import datetime
import uuid
from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Cookie
from pydantic import BaseModel
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from chat.core.models import TestMessages, Guest, Room, Message
from chat.core.schemas import MessagesModel, NameSchema
from chat.database.db import async_session_maker, get_async_session

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.get("/get_user/")
async def get_user(guest_id: str = Cookie(None), db: AsyncSession = Depends(get_async_session)):
    if guest_id:
        async with db as session:
            query = select(Guest).where(Guest.guest_id == guest_id)
            result = await session.execute(query)
            guest = result.scalars().first()

        if guest:

            return guest
        else:
            return {"id": 10, 'name': 'Unknown'}

    return {"id": 10, 'name': 'Unknown'}


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, add_to_db: bool, room_id: int):
        if add_to_db:
            await self.add_messages_to_database(message, room_id)
        for connection in self.active_connections:
            await connection.send_text(message)

    @staticmethod
    async def add_messages_to_database(message: str, room_id: int):
        async with async_session_maker() as session:
            stmt = insert(Message).values(
                content=message,
                room_id=room_id
            )
            await session.execute(stmt)
            await session.commit()


manager = ConnectionManager()


@router.get("/last_messages")
async def get_last_messages(
        session: AsyncSession = Depends(get_async_session),
) -> List[MessagesModel]:
    query = select(TestMessages).order_by(TestMessages.id.desc())
    messages = await session.execute(query)
    return messages.scalars().all()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int, guest: Guest = Depends(get_user)):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{guest}: {data}", add_to_db=True)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{guest} left the chat", add_to_db=False)


""" Guest """


@router.post("/set_name/")
async def set_name(name_data: NameSchema, db: AsyncSession = Depends(get_async_session)):
    name = name_data.name
    guest_id = str(uuid.uuid4())
    guest = Guest(name=name, guest_id=guest_id)
    print(guest)
    db.add(guest)
    await db.commit()
    await db.close()
    response = JSONResponse(content={'name': guest.name})
    response.set_cookie(key='guest_id', value=guest.guest_id, max_age=3600000)
    return response


@router.get("/get_name/")
async def get_name(guest: Guest = Depends(get_user)):
    return {"name": guest.name}


""" Rooms """


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


""" Messages """


@router.get("/get_room_messages/{room_id}")
async def get_room_messages(room_id: int,
                            session: AsyncSession = Depends(get_async_session),
                            ) -> List[MessagesModel]:
    query = select(Message).where(Message.room_id == room_id).order_by(Message.id.desc())
    messages = await session.execute(query)
    return messages.scalars().all()


@router.websocket("/send_message/{room_id}")
async def send_message(websocket: WebSocket, room_id: int, guest: Guest = Depends(get_user),
                       db: AsyncSession = Depends(get_async_session)):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            async with db as session:
                query = select(Guest).where(Guest.id == guest["id"])
                result = await session.execute(query)
                sender = result.scalars().first()
                message = Message(content=data, room_id=room_id)
                sender.messages.append(message)
                session.add(message)
                session.add(sender)
                await session.commit()

            await manager.broadcast(f"{guest['name']}: {data}", add_to_db=True, room_id=room_id)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{guest['name']} left the chat", add_to_db=False, room_id=room_id)
