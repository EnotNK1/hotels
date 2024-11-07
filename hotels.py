from fastapi import Query, Body, APIRouter

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Сочи", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"}
]

@router.get("",
         summary="Получить список отелей",
         description="Можно отправить опционально id и/или название отеля для дополнительной фильтрации")
def get_hotels(
        id: int | None = Query(None, description="Идентификатор"),
        title: str | None = Query(None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel[title] != title:
            continue
        hotels_.append(hotel)
        return hotels_

@router.post("",
          summary="Создать отель")
def create_hotel(
        title: str = Body(embed=True),
        name: str = Body(embed=True),
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title,
        "name": name
    })
    return {"status": "OK"}

@router.put("/{hotel_id}",
         summary="Обновить информацию об отеле полностью")
def put_hotel(
        hotel_id: int,
        title: str = Body(embed=True),
        name: str = Body(embed=True),
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            break
    return {"status": "OK"}

@router.patch("/{hotel_id}",
           summary="Обновить информацию об отеле частично")
def patch_hotel(
        hotel_id: int,
        title: str | None = Body(default=None, embed=True),
        name: str | None = Body(default=None, embed=True),
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title is not None:
                hotel["title"] = title
            if name is not None:
                hotel["name"] = name
            break
    return {"status": "OK"}


@router.delete("/{hotel_id}",
            summary="Удалить отель")
def delete_notel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}