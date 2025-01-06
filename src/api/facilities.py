from fastapi import APIRouter, Body, Query
from datetime import date

from src.api.dependencies import DBDep
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.facilities import FacilityAdd, Facility
from src.schemas.rooms import RoomPatchRequest, RoomAddRequest, RoomAdd, RoomPatch

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("",
         summary="Получить список удобств",
         description="")
async def get_facilities(
        db: DBDep,
):
        return await db.facilities.get_all()



@router.post("",
          summary="Создать удобство")
async def create_facility(db: DBDep, facility_data: FacilityAdd = Body(openapi_examples={
    "1": {
        "summary": "спа",
        "value": {
            "title": "спа",
        }
    }
})):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    return {"status": "OK", "data": facility}



