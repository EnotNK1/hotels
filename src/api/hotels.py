from fastapi import Query, APIRouter, Body

from src.database import async_session_maker
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
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )



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
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}",
         summary="Обновить информацию об отеле полностью")
async def put_hotel(hotel_id: int, hotel_data: Hotel = Body(openapi_examples={
    "1": { "summary": "Сочи", "value": {
        "title": "Сочи 5 звезд отель у моря",
        "location": "sochi_u_morya"
    }},
    "2": { "summary": "Дубай", "value": {
        "title": "Дубай 5 звезд отель",
        "location": "dubai"
    }},
})):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()

    return {"status": "OK"}


@router.patch("/{hotel_id}",
           summary="Обновить информацию об отеле частично")
async def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}",
            summary="Удалить отель")
async def delete_notel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()

    return {"status": "OK"}