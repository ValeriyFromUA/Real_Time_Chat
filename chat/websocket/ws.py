from typing import List

from fastapi import WebSocket

from sqlalchemy import insert

from chat.database.db import async_session_maker
from chat.message.models import Message


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
