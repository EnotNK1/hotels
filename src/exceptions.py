class MyAppException(Exception):
    detail = "Неожиданная ошибка"
    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(MyAppException):
    detail = "Объект не найден"


class AllRoomsAreBookedException(MyAppException):
    detail = "Не осталось свободных номеров"