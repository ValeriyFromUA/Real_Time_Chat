import uuid

from fastapi import APIRouter, Cookie, Depends, HTTPException
from fastapi.exceptions import ResponseValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from chat.database.db import get_async_session
from chat.guest.models import Guest
from chat.guest.schemas import GuestSchema, SetGuestSchema

router = APIRouter(
    prefix="/guests",
    tags=["Guest"]
)


@router.get("/current_user")
async def current_user(guest_uuid: str = Cookie(None), db: AsyncSession = Depends(get_async_session)):
    if guest_uuid:
        async with db as session:
            query = select(Guest).where(Guest.guest_uuid == guest_uuid)
            result = await session.execute(query)
            guest = result.scalars().first()

        if guest:
            return guest

        raise HTTPException(status_code=404, detail=f"Guest not found")
    raise HTTPException(status_code=404, detail=f"Guest not found")


@router.post("/create")
async def create_user(name_data: SetGuestSchema, db: AsyncSession = Depends(get_async_session)):
    name = name_data.name
    guest_uuid = str(uuid.uuid4())
    guest = Guest(name=name, guest_uuid=guest_uuid)
    db.add(guest)
    await db.commit()
    await db.close()
    response = JSONResponse(content={'name': guest.name, 'id': guest.id})
    response.set_cookie(key='guest_uuid', value=guest.guest_uuid, max_age=3600000)
    return response


@router.put("/change_name")
async def change_name(name_data: SetGuestSchema, guest_uuid: str = Cookie(None),
                      db: AsyncSession = Depends(get_async_session)):
    new_name = name_data.name

    guest = await db.execute(select(Guest).where(Guest.guest_uuid == guest_uuid))
    guest = guest.scalar()

    if not guest:
        raise HTTPException(status_code=404, detail=f"Guest with id {guest_uuid} not found")
    guest.name = new_name

    await db.commit()
    await db.close()

    response = JSONResponse(content={'name': guest.name})
    response.set_cookie(key='guest_uuid', value=guest.guest_uuid, max_age=3600000)
    return response


@router.get("/{guest_id}", response_model=GuestSchema)
async def get_user(guest_id: int, db: AsyncSession = Depends(get_async_session)):
    async with db as session:
        query = select(Guest).where(Guest.id == guest_id)
        result = await session.execute(query)
        guest = result.scalars().first()
        if guest:
            return guest

        raise HTTPException(status_code=404, detail=f"Guest with id {guest_id} not found")


@router.delete("/{guest_id}/delete", response_model=dict)
async def delete_user(guest_id: int, db: AsyncSession = Depends(get_async_session)):
    async with db as session:
        query = select(Guest).where(Guest.id == guest_id)
        result = await session.execute(query)
        guest = result.scalars().first()
        if guest:
            deleted_guest_info = {
                "status_code": 204,
                "id": guest.id,
                "name": guest.name,
                "message": f"Guest with id {guest_id} deleted successfully"
            }
            await session.delete(guest)
            await session.commit()
            return deleted_guest_info

        raise HTTPException(status_code=404, detail=f"Guest with id {guest_id} not found")


@router.get("/", response_model=list[GuestSchema])
async def get_users(db: AsyncSession = Depends(get_async_session)):
    async with db as session:
        query = select(Guest)
        result = await session.execute(query)
        guests = result.scalars().all()
        if guests:
            return guests

        raise HTTPException(status_code=404, detail=f"Guests not found")
