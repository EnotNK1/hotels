import shutil
from fastapi import APIRouter, UploadFile

from src.services.images import ImagesService
from src.tasks.tasks import resize_image

router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post("")
def upload_image(file: UploadFile):
    ImagesService().upload_image(file)
