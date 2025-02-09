from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache
from datetime import date

from src.api.dependencies import DBDep
from src.exceptions import HotelNotFoundHTTPException, RoomNotFoundHTTPException, HotelNotFoundException, RoomNotFoundException
from src.schemas.rooms import RoomPatchRequest, RoomAddRequest
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Комнаты"])


@router.get("/{hotel_id}/rooms", summary="Получить список комнат", description="")
@cache(expire=10)
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
):
    return await RoomService(db).get_filtered_by_time(hotel_id, date_from, date_to)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить комнату по id")
@cache(expire=10)
async def get_room_by_id(db: DBDep, hotel_id: int, room_id: int):
    try:
        return await RoomService(db).get_room(room_id, hotel_id=hotel_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post("/{hotel_id}/rooms", summary="Создать комнату")
async def create_room(
    db: DBDep,
    hotel_id: int,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Комфорт",
                "value": {
                    "title": "Комфорт",
                    "description": "Комфортная команата",
                    "price": 7900,
                    "quantity": 15,
                    "facilities_ids": [1, 2],
                },
            }
        }
    ),
):
    try:
        room = await RoomService(db).create_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {"status": "OK", "data": room}


@router.put(
    "/{hotel_id}/rooms/{room_id}", summary="Обновить информацию о комнате полностью"
)
async def put_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Люкс",
                "value": {
                    "title": "Люкс",
                    "description": "Люкс команата",
                    "price": 18900,
                    "quantity": 5,
                    "facilities_ids": [1, 2],
                },
            }
        }
    ),
):
    await RoomService(db).edit_room(hotel_id, room_id, room_data)

    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}", summary="Обновить информацию о комнате частично"
)
async def patch_room(
    db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest
):
    await RoomService(db).partially_edit_room(hotel_id, room_id, room_data)
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить комнату")
async def delete_notel(db: DBDep, hotel_id: int, room_id: int):
    await RoomService(db).delete_room(hotel_id, room_id)

    return {"status": "OK"}
