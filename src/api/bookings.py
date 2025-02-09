from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache

from src.exceptions import AllRoomsAreBookedException, AllRoomsAreBookedHTTPException
from src.schemas.bookings import BookingAddRequest
from src.api.dependencies import UserIdDep, DBDep
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("", summary="Создать бронирование")
async def create_booking(
    db: DBDep, user_id: UserIdDep, booking_data: BookingAddRequest
):
    try:
        booking = await BookingService(db).add_booking(user_id, booking_data)
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException

    return {"status": "OK", "data": booking}


@router.get("", summary="Получить список всех бронирований", description="")
@cache(expire=10)
async def get_bookings(db: DBDep):
    return await BookingService(db).get_bookings()


@router.get("/me", summary="Получить список моих бронирований", description="")
@cache(expire=10)
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    return await BookingService(db).get_my_bookings(user_id)
