from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import not_

from app.models import User


class CRUDBase:
    """Базовый класс для CRUD-операций."""

    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        """Получение объекта по его id."""
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_all(
            self,
            session: AsyncSession
    ):
        """Получение всех объектов."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None,
            commit: bool = True,
    ):
        """Создание объекта."""
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            session: AsyncSession,
            obj_in=None,
    ):
        """Обновление объекта."""
        if obj_in:
            obj_data = jsonable_encoder(db_obj)
            update_data = obj_in.dict(exclude_unset=True)

            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ):
        """Удаление объекта."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_not_closed(self, session: AsyncSession):
        result = await session.execute(
            select(self.model).where(not_(self.model.fully_invested))
        )
        return result.scalars().all()