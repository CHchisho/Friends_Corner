from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from database import get_async_session

from PIL import Image
from io import BytesIO


def convert_to_jpeg(image_bytes):
    image = Image.open(BytesIO(image_bytes))
    # Сохраняем изображение в формате JPEG
    output = BytesIO()
    image.convert("RGB").save(output, format="JPEG")
    return output.getvalue()

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
