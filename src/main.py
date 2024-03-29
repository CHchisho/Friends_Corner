from fastapi import FastAPI, UploadFile, File, Request, Depends
from fastapi.middleware.cors import CORSMiddleware

from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from auth.models import User
from sqlalchemy import insert, select, asc, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from database import async_session_maker, get_async_session


from auth.utils import convert_to_jpeg
from tasks.router import router as router_tasks
from pages.router import router as router_pages
from chat.router import router as router_chat
from redis import asyncio as aioredis

from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
import asyncio

app = FastAPI(
    title="Trading App"
)

# HTML+CSS+JS
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_tasks)
app.include_router(router_pages)
app.include_router(router_chat)

origins = [
    "http://localhost:51974",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin", "Authorization"],
)



# @app.post("/auth/photos")
# async def upload_files(file1: UploadFile = File(...), file2: UploadFile = File(...)):
#     try:
#         file1_data = convert_to_jpeg(file1.file.read())
#         file2_data = convert_to_jpeg(file2.file.read())
#
#         with open("static/photos/new_photo_1.jpg", "wb") as f1:
#             f1.write(file1_data)
#         with open("static/photos/new_photo_2.jpg", "wb") as f2:
#             f2.write(file2_data)
#     finally:
#         return {"status": 201}
@app.post("/auth/photos")
async def upload_files(file1: UploadFile = File(...), file2: UploadFile = File(...),session: AsyncSession = Depends(get_async_session)):

    query = select(User.id).order_by(User.id.desc()).limit(1)
    last_id = await session.execute(query)
    last_id = last_id.first()[0]
    try:
        file1_data = convert_to_jpeg(file1.file.read())
        file2_data = convert_to_jpeg(file2.file.read())

        with open(f"static/photos/{last_id+1}_1.jpg", "wb") as f1:
            f1.write(file1_data)
        with open(f"static/photos/{last_id+1}_2.jpg", "wb") as f2:
            f2.write(file2_data)

        print("created photos: ", last_id+1)
    finally:
        print({"status": 201})
        return {"status": 201}

@app.get("/")
def first_page(request: Request):
    return templates.TemplateResponse("index.html",{"request": request})



# Обязательные для запуска
# При запуске сервера, запуск redis
@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    # asyncio.create_task(user_data_reset())

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    return templates.TemplateResponse("404.html", {"request": request})



# Mini project rendering
@app.get("/luksia")
def luksia_page(request: Request):
    return templates.TemplateResponse("luksia_page.html", {"request": request})
@app.get("/luksia_v2")
def luksia_v2_page(request: Request):
    return templates.TemplateResponse("luksia_page_new.html", {"request": request})

