from fastapi import APIRouter, Body

from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd
from src.services.facilities import FacilityService

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Получить список удобств", description="")
@cache(expire=10)
async def get_facilities(
    db: DBDep,
):
    return await FacilityService(db).get_all()


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
    facility = await FacilityService(db).create_facility(facility_data)

    return {"status": "OK", "data": facility}
