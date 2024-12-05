from sqlalchemy import select, insert, delete, update
from pydantic import BaseModel
from fastapi import HTTPException


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_filtred(self, *filter, **filtred_by):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filtred_by)
        )
        result = await self.session.execute(query)

        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtred()


    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)

        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model, from_attributes=True)


    async def add(self, data: BaseModel):
        data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(data_stmt)
        model = result.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)

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