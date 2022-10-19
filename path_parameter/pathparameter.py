import uvicorn
from fastapi import FastAPI, Path
from enum import Enum


class EnumClass(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()


@app.get("/")
async def hello_world():
    return {"message": "Hello World"}


@app.get("/items/{item_name}")
def give_item_name(item_name: int):
    return {"item": item_name}


@app.get("/enum/example/{modalName}")
def enum_example(modal_name: EnumClass):
    if modal_name is EnumClass.alexnet:
        return {"modalName": modal_name}
    elif modal_name is EnumClass.resnet:
        return {"modalName": modal_name}
    elif modal_name.value == "lenet":
        return {"modalName": modal_name}


# we can give same arguments like min/max_length/regex/alias and meta information title/description to Path() too we
# can some special args like ge(greater than or equal) le(less than or equal) gt(greater than) lt(less than) we have
# to provide * as first arg that will allow us to have args with no default value after the args which has default
# value if don't provide it that python will complain, second solution is to reorder the args place args with no
# default first
@app.get("/item/{item_id}")
def get_item_id(*, item_id: int = Path(ge=0, le=100), q: str):
    return {"p": item_id, "q": q}


if __name__ == "__main__":
    uvicorn.run(
        "path_parameter:app", host="localhost", port=8000, reload=True, workers=3
    )
