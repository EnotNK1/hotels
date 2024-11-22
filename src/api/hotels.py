from shutil import which

from fastapi import Query, APIRouter, Body

from sqlalchemy import  insert, select, func
from sqlalchemy.util import await_only

from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep

router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get("",
         summary="Получить список отелей",
         description="Можно отправить опционально адрес и/или название отеля для дополнительной фильтрации.<p>Tак же есть"
                     " возможность пагинации, ограничения: page > 0, 1 < per_page < 30 </p>")
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(default=None, description="Адрес отеля"),
        title: str | None = Query(default=None, description="Название отеля"),
):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all()
    # per_page = pagination.per_page or 5
    # async with async_session_maker() as  session:
    #     query = select(HotelsOrm)
    #     if location:
    #         query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
    #     if title:
    #         query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
    #     query = (
    #         query
    #         .limit(per_page)
    #         .offset(per_page * (pagination.page - 1))
    #     )
    #     result = await session.execute(query)
    #
    #     hotels = result.scalars().all()
    #     return hotels


@router.post("",
          summary="Создать отель")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {
        "summary": "Томск",
        "value": {
            "title": "Отель 5 звезд",
            "location": "ул. Вершинина 74"
        }
    }
})):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "OK"}


@router.put("/{hotel_id}",
         summary="Обновить информацию об отеле полностью")
def put_hotel(hotel_id: int, hotel_data: Hotel = Body(openapi_examples={
    "1": { "summary": "Сочи", "value": {
        "title": "Сочи 5 звезд отель у моря",
        "name": "sochi_u_morya"
    }},
    "2": { "summary": "Дубай", "value": {
        "title": "Дубай 5 звезд отель",
        "name": "dubai"
    }},
})):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
            break
    return {"status": "OK"}


@router.patch("/{hotel_id}",
           summary="Обновить информацию об отеле частично")
def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title is not None:
                hotel["title"] = hotel_data.title
            if hotel_data.name is not None:
                hotel["name"] = hotel_data.name
            break
    return {"status": "OK"}


@router.delete("/{hotel_id}",
            summary="Удалить отель")
def delete_notel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}