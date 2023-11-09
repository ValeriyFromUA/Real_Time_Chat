import uuid

from fastapi import APIRouter, Cookie, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from chat.database.db import get_async_session
from chat.guest.models import Guest
from chat.guest.schemas import GuestSchema

router = APIRouter(
    prefix="/guests",
    tags=["Guest"]
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


@router.post("/set_name/")
async def set_name(name_data: GuestSchema, db: AsyncSession = Depends(get_async_session)):
    name = name_data.name
    guest_id = str(uuid.uuid4())
    guest = Guest(name=name, guest_id=guest_id)
    db.add(guest)
    await db.commit()
    await db.close()
    response = JSONResponse(content={'name': guest.name})
    response.set_cookie(key='guest_id', value=guest.guest_id, max_age=3600000)
    return response


@router.get("/get_name/")
async def get_name(guest: Guest = Depends(get_user)):
    return {"name": guest.name}
