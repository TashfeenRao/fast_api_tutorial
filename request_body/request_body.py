import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str = None
    price: int
    tax: int = None


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


if __name__ == "__main__":
    uvicorn.run(
        "request_body:app",
        host="localhost",
        port=8000,
        reload=True,
        debug=True,
        workers=3,
    )
