from datetime import date

from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache

from src.exceptions import ObjectNotFoundException, HotelNotFoundHTTPException
from src.schemas.hotels import HotelPatch, HotelAdd
from src.api.dependencies import PaginationDep
from src.api.dependencies import DBDep
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "",
    summary="Получить список отелей",
    description="Можно отправить опционально адрес и/или название отеля для дополнительной фильтрации.<p>Tак же есть"
    " возможность пагинации, ограничения: page > 0, 1 < per_page < 30 </p>",
)
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(default=None, description="Адрес отеля"),
    title: str | None = Query(default=None, description="Название отеля"),
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
):
    return await HotelService(db).get_filtered_by_time(
        pagination,
        location,
        title,
        date_from,
        date_to,
    )


@router.get("/{hotel_id}", summary="Получить отель по id")
@cache(expire=10)
async def get_hotel_by_id(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("", summary="Создать отель")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Томск",
                "value": {"title": "Отель 5 звезд", "location": "ул. Вершинина 74"},
            }
        }
    ),
):
    hotel = await HotelService(db).add_hotel(hotel_data)

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Обновить информацию об отеле полностью")
async def put_hotel(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Сочи 5 звезд отель у моря",
                    "location": "sochi_u_morya",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {"title": "Дубай 5 звезд отель", "location": "dubai"},
            },
        }
    ),
):
    await HotelService(db).edit_hotel(hotel_id, hotel_data)

    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Обновить информацию об отеле частично")
async def patch_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPatch):
    await HotelService(db).edit_hotel_partially(hotel_id, hotel_data, exclude_unset=True)
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удалить отель")
async def delete_notel(db: DBDep, hotel_id: int):
    await HotelService(db).delete_hotel(hotel_id)

    return {"status": "OK"}
