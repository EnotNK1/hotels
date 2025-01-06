from fastapi import APIRouter, Body, Query
from datetime import date

from src.api.dependencies import DBDep
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomPatchRequest, RoomAddRequest, RoomAdd, RoomPatch

router = APIRouter(prefix="/hotels", tags=["Комнаты"])

@router.get("/{hotel_id}/rooms",
         summary="Получить список комнат",
         description="")
async def get_rooms(
        db: DBDep,
        hotel_id: int,
        date_from: date = Query(example="2024-08-01"),
        date_to: date = Query(example="2024-08-10"),
):
        return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

@router.get("/{hotel_id}/rooms/{room_id}",
            summary="Получить комнату по id")
async def get_room_by_id(db: DBDep, hotel_id: int, room_id: int):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms",
          summary="Создать комнату")
async def create_room(db: DBDep, hotel_id: int, room_data: RoomAddRequest = Body(openapi_examples={
    "1": {
        "summary": "Комфорт",
        "value": {
            "title": "Комфорт",
            "description": "Комфортная команата",
            "price": 7900,
            "quantity": 15,
        }
    }
})):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}",
         summary="Обновить информацию о комнате полностью")
async def put_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest = Body(openapi_examples={
    "1": {
        "summary": "Люкс",
        "value": {
            "title": "Люкс",
            "description": "Люкс команата",
            "price": 18900,
            "quantity": 5,
        }
    }
})):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id, hotel_id=hotel_id)
    await db.commit()

    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}",
           summary="Обновить информацию о комнате частично")
async def patch_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}",
            summary="Удалить комнату")
async def delete_notel(db: DBDep, hotel_id: int, room_id: int):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()

    return {"status": "OK"}