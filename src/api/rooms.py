from fastapi import APIRouter, Body

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomPatchRequest, RoomAddRequest, RoomAdd, RoomPatch

router = APIRouter(prefix="/hotels", tags=["Комнаты"])

@router.get("/{hotel_id}/rooms",
         summary="Получить список комнат",
         description="")
async def get_rooms(
        hotel_id: int,
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtred(hotel_id=hotel_id)

@router.get("/{hotel_id}/rooms/{room_id}",
            summary="Получить комнату по id")
async def get_room_by_id(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)
    return room


@router.post("/{hotel_id}/rooms",
          summary="Создать комнату")
async def create_room(hotel_id: int, room_data: RoomPatchRequest = Body(openapi_examples={
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
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}",
         summary="Обновить информацию о комнате полностью")
async def put_room(hotel_id: int, room_id: int, room_data: RoomAddRequest = Body(openapi_examples={
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
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data, id=room_id, hotel_id=hotel_id)
        await session.commit()

    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}",
           summary="Обновить информацию о комнате частично")
async def patch_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}",
            summary="Удалить комнату")
async def delete_notel(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()

    return {"status": "OK"}