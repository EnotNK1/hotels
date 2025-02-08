from datetime import date
from fastapi import HTTPException

class MyAppException(Exception):
    detail = "Неожиданная ошибка"
    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(MyAppException):
    detail = "Объект не найден"


class ObjectAlreadyExistsException(MyAppException):
    detail = "Похожий объект уже существует"


class AllRoomsAreBookedException(MyAppException):
    detail = "Не осталось свободных номеров"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail="Дата заезда не может быть позже даты выезда")


class MyAppExceptionHTTPException(HTTPException):
    status_code = 500
    detail = None
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(MyAppException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(MyAppException):
    status_code = 404
    detail = "Номер не найден"