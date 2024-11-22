from sqlalchemy import select, insert, delete, update
from pydantic import BaseModel
from fastapi import HTTPException

class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)

        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)

        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(data_stmt)
        return result.scalars().one()

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        query = select(self.model).filter_by(**filter_by)

        result = await self.session.execute(query)
        items = result.scalars().all()

        if len(items) == 0:
            raise HTTPException(status_code=404, detail="Объект не найден")
        elif len(items) > 1:
            raise HTTPException(status_code=400, detail="Найдено несколько объектов")

        edit_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(edit_stmt)

    async def delete(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)

        result = await self.session.execute(query)
        items = result.scalars().all()

        if len(items) == 0:
            raise HTTPException(status_code=404, detail="Объект не найден")
        elif len(items) > 1:
            raise HTTPException(status_code=400, detail="Найдено несколько объектов")

        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)