from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from auth.base_config import auth_backend, fastapi_users
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

@router.get("/me")
def get_search_page(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse("me.html", {"request": request,
            "userdata": {"id": user.id,
                         "email": user.email,
                         "age": user.your_age,
                         "username": user.username,
                         "gender": user.gender,
                         "about_you": user.about_you,
                         "hobbies": user.hobbies,
                         "regions": user.regions,
                         "phone_number": user.phone_number,}})

@router.get("/chat")
def get_chat_page(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse("chat.html", {"request": request, "userdata": {"id":user.id, "email":user.email, "age":user.your_age,"username":user.username}})



@router.get("/match")
def get_match_page(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse("match.html", {"request": request,
            "userdata": {"id": user.id,
                         "email": user.email,
                         "age": user.your_age,
                         "username": user.username}})

