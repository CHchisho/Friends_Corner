# from fastapi import FastAPI
# app = FastAPI()
#
# users = [
#     {'id':1, "name":"Ilia1"},
#     {'id':2, "name":"Ilia2"},
#     {'id':3, "name":"Ilia3"}
# ]
#
# @app.get("/users/{user_id}")
# def hello(user_id: int):
#     return [user for user in users if user.get("id") == user_id]
#
#
# @app.post("/users/{user_id}")
# def change_name(user_id: int, name: str):
#     data_user = [user for user in users if user.get("id") == user_id][0]
#     data_user["name"] = name
#     return {"status": 200, "data": data_user}
#
# @app.get("/test/{id}")
# def test(id: int):
#     return {"status": 200, "data": id}

from enum import Enum
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


app = FastAPI()


@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
