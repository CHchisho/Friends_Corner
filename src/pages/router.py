from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from operations.router import get_specific_operations

from pydantic import BaseModel



router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/base")
def get_base_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

# @router.get("/search/{operation_type}")
# def get_search_page(request: Request, operations=Depends(get_specific_operations)):
#     return (templates.TemplateResponse("search.html", {"request": request, "operations": operations["data"]})

@router.get("/search")
def get_search_page(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})

@router.get("/new_user")
def get_base_page(request: Request):
    return templates.TemplateResponse("new_user.html", {"request": request})


class User(BaseModel):
    id_2: str

@router.post("/search_api/{item_id}")
def get_search_api(item_id: int, q: User):
    print(item_id)
    print(q)
    return {"item_id": item_id+1, "q": item_id}
