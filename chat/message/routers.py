from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from chat.database.db import get_async_session
from chat.guest.models import Guest
from chat.guest.routers import get_user
from chat.message.models import Message
from chat.message.schemas import MessagesModel
from chat.websocket.ws import manager

router = APIRouter(
    prefix="/messages",
    tags=["Messages"]
)


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
