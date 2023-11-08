import datetime
import uuid
from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Cookie
from pydantic import BaseModel
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from chat.core.models import TestMessages, Guest
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
            return {"message": "Користувач не знайдений"}

    return {"message": "Користувач не ідентифікований"}


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

    async def broadcast(self, message: str, add_to_db: bool):
        if add_to_db:
            await self.add_messages_to_database(message)
        for connection in self.active_connections:
            await connection.send_text(message)

    @staticmethod
    async def add_messages_to_database(message: str):
        async with async_session_maker() as session:
            stmt = insert(TestMessages).values(
                message=message
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
            print(websocket)
            print(guest)
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
