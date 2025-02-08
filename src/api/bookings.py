from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache

from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException, RoomNotFoundHTTPException
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.api.dependencies import UserIdDep, DBDep

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("", summary="Создать бронирование")
async def create_booking(
    db: DBDep, user_id: UserIdDep, booking_data: BookingAddRequest
):
    try:

        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException

    hotel = await db.hotels.get_one(id=room.hotel_id)
    _booking_data = BookingAdd(
        price=room.price, user_id=user_id, **booking_data.model_dump()
    )
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    await db.commit()

    return {"status": "OK", "data": booking}


@router.get("", summary="Получить список всех бронирований", description="")
@cache(expire=10)
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me", summary="Получить список моих бронирований", description="")
@cache(expire=10)
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_filtred(user_id=user_id)
