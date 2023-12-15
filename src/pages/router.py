from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from auth.base_config import auth_backend, fastapi_users
from operations.router import get_specific_operations
from auth.models import User

from pydantic import BaseModel



router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="templates")

# @router.get("/base")
# def get_base_page(request: Request):
#     return templates.TemplateResponse("base.html", {"request": request})

# @router.get("/search/{operation_type}")
# def get_search_page(request: Request, operations=Depends(get_specific_operations)):
#     return (templates.TemplateResponse("search.html", {"request": request, "operations": operations["data"]}))

# @router.get("/search")
# def get_search_page(request: Request):
#     return templates.TemplateResponse("search.html", {"request": request})

@router.get("/new_user")
def get_new_user_page(request: Request):
    return (templates.TemplateResponse("new_user.html", {"request": request}))


@router.get("/login")
def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


current_user = fastapi_users.current_user()

@router.get("/search")
def get_search_page(request: Request, user: User = Depends(current_user)):
    # print(user.username)
    # print(user.your_age)
    # print(user.email)
    # print(user.id)
    # print(type(user))

    return (templates.TemplateResponse("search.html", {"request": request, "userdata": {"id":user.id, "email":user.email, "age":user.your_age,"username":user.username}}))



class User(BaseModel):
    email: str
    password: str
    is_active: int
    is_superuser: int
    is_verified: int
    username: str
    phonenumber: str
    gender: str
    regions: str
    your_age: int
    hobby: list
    friend_gender: str
    friend_age: int


@router.post("/search_api/")
def get_search_api(q: User):
    # print('пост зарпос')
    # print(id)
    print(q)
    return {"qdata": str(q)}

# class Item(BaseModel):
#     qwe: int
# @router.post("/search_api/{page_id}")
# async def search_api(page_id: int, item: Item, request: Request):
#     data = await request.json()
#     qwe = data.get("qwe")
#
#     return {"message": "Data processed"}
# @router.exception_handler(404)
# async def custom_404_handler(request, __):
#     return templates.TemplateResponse("404.html", {"request": request})