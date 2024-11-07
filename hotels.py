from fastapi import Query, APIRouter, Body
from schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Сочи", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"}
]

@router.get("",
         summary="Получить список отелей",
         description="Можно отправить опционально id и/или название отеля для дополнительной фильтрации.<p>Tак же есть"
                     " возможность пагинации, ограничения: page > 0, 1 < per_page < 30 </p>")
def get_hotels(
        id: int | None = Query(None, description="Идентификатор"),
        title: str | None = Query(None, description="Название отеля"),
        page: int | None = Query(None, gt=0, description="Номер страницы"),
        per_page: int | None = Query(None, gt=1, lt=30, description="Количество отелей на странице"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel[title] != title:
            continue
        hotels_.append(hotel)

    if page and per_page:
        return hotels_[per_page * (page - 1):][:per_page]

    return hotels_


@router.post("",
          summary="Создать отель")
def create_hotel(hotel_data: Hotel):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })
    return {"status": "OK"}


@router.put("/{hotel_id}",
         summary="Обновить информацию об отеле полностью")
def put_hotel(hotel_id: int, hotel_data: Hotel = Body(openapi_examples={
    "1": { "summary": "Сочи", "value": {
        "title": "Сочи 5 звезд отель у моря",
        "name": "sochi_u_morya"
    }},
    "2": { "summary": "Дубай", "value": {
        "title": "Дубай 5 звезд отель",
        "name": "dubai"
    }},
})):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
            break
    return {"status": "OK"}


@router.patch("/{hotel_id}",
           summary="Обновить информацию об отеле частично")
def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title is not None:
                hotel["title"] = hotel_data.title
            if hotel_data.name is not None:
                hotel["name"] = hotel_data.name
            break
    return {"status": "OK"}


@router.delete("/{hotel_id}",
            summary="Удалить отель")
def delete_notel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}