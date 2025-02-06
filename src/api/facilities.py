from fastapi import APIRouter, Body

from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Получить список удобств", description="")
@cache(expire=10)
async def get_facilities(
    db: DBDep,
):
    return await db.facilities.get_all()


@router.post("", summary="Создать удобство")
async def create_facility(
    db: DBDep,
    facility_data: FacilityAdd = Body(
        openapi_examples={
            "1": {
                "summary": "спа",
                "value": {
                    "title": "спа",
                },
            }
        }
    ),
):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    return {"status": "OK", "data": facility}
