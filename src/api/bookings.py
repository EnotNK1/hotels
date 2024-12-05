from fastapi import APIRouter
from sqlalchemy.testing.config import db_url

from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.api.dependencies import UserIdDep, DBDep

router = APIRouter(prefix="/bookings", tags=["Бронирования"])

@router.post("", summary="Создать бронирование")
async def create_booking(
        db: DBDep,
        user_id: UserIdDep,
        booking_data: BookingAddRequest
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    _booking_data = BookingAdd(price=room.price, user_id=user_id, **booking_data.model_dump())
    booking = await db.bookings.add(_booking_data)
    await db.commit()

    return {"status": "OK", "data": booking}

