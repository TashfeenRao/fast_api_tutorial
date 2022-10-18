import uvicorn
from fastapi import FastAPI, Path, Body, Query
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str = None
    price: int
    tax: int = None


class User(BaseModel):
    name: str
    age: int
    post: str


app = FastAPI()


@app.get("/")
def hello_world():
    return {"message": "hello world"}


# we can create pydantic modal/schema and use it as type in this way we can validate in comming request body
# pydantic converts the modal to corresponding types and than to Json and than do matching
# request body will be pydantic modal not dict we can convert it to dict after receiving it
@app.post("/save/item")
def save_item(item: Item):
    dict_item = item.dict()
    print(item.name)
    print(item.price)
    print(item.description)
    if dict_item:
        return {"item": item}
    return item


# we can use all path, query and request body at a same time; fastapi is smart enough to differentiate between them
# if path parameter match than it will be consider as path params, if it is singular value like 'int/float/string'
# and does not matches in provided variable than it will be query param.
# if data is coming as dict from the request body
@app.post("/item/{name}")
def all_params(name: str, item: Item, q: int = None):
    item_dict = item.dict()
    return {"path_parameter": name, "query_params": q, "item": item}


# we can use fastapi built in Body() func to do all the validation that it provides like min/max_length/regex/alias
# and meta information title/description we can use mix of path, query and body params fastapi is smart enough to
# recognise who is what we can use multiple pydantic modals for request body we can embed more properties in the
# request body using the Body(embed=True)
@app.post("/user/{user_id}/item/{item_id}")
def multiple_user_body_params(
    *,
    user_id: int = Path(),
    item_id: int = Path(),
    item: Item = Body(),
    user: User = Body(),
    q: str | None = Query(default=None),
    approval: bool = Body(default=False, embed=True)
):
    return {user_id, item_id, item, user}


if __name__ == "__main__":
    uvicorn.run(
        "request_body:app",
        host="localhost",
        port=8000,
        reload=True,
        debug=True,
        workers=3,
    )
