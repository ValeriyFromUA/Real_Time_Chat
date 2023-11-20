from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from chat.category.models import Category
from chat.category.schemas import CategorySchema, CategoryRoomSchema, CategoryUpdateSchema
from chat.database.db import get_async_session

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.post("/create", response_model=CategorySchema)
async def create_category(category_name: str, description: str = "", db: AsyncSession = Depends(get_async_session)):
    category = Category(name=category_name, description=description)
    db.add(category)
    await db.commit()
    return category


@router.get("/", response_model=list[CategoryRoomSchema])
async def get_categories(db: AsyncSession = Depends(get_async_session)):
    async with db as session:
        query = select(Category).options(selectinload(Category.rooms))
        result = await session.execute(query)

    categories = result.scalars().all()

    return jsonable_encoder(categories)


@router.get("/{category_id}", response_model=CategoryRoomSchema)
async def get_category(category_id: int, db: AsyncSession = Depends(get_async_session)):
    async with db as session:
        query = select(Category).where(Category.id == category_id).options(selectinload(Category.rooms))
        result = await session.execute(query)
        category = result.scalars().first()
        if category:
            return category

        raise HTTPException(status_code=404, detail=f"Category with id {category_id} not found")


@router.delete("/{category_id}/delete", response_model=dict)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_async_session)):
    async with db as session:
        query = select(Category).where(Category.id == category_id)
        result = await session.execute(query)
        category = result.scalars().first()
        if category:
            deleted_guest_info = {
                "status_code": 204,
                "id": category.id,
                "name": category.name,
                "message": f"Category with id {category_id} deleted successfully"
            }
            await session.delete(category)
            await session.commit()
            return deleted_guest_info

        raise HTTPException(status_code=404, detail=f"Category with id {category_id} not found")


@router.put("/{category_id}/update", response_model=CategorySchema)
async def update_category(category_id: int, category_data: CategoryUpdateSchema,
                          db: AsyncSession = Depends(get_async_session)):
    new_name = category_data.name
    new_description = category_data.description

    category = await db.execute(select(Category).where(Category.id == category_id))
    category = category.scalar()

    if not category:
        raise HTTPException(status_code=404, detail=f"Category with id {category_id} not found")
    category.name = new_name
    category.description = new_description

    await db.commit()
    await db.close()

    return category
