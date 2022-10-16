from fastapi import FastAPI
from enum import Enum


class EnumClass(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()


@app.get('/')
async def hello_world():
    return {"message": "Hello World"}

@app.get('/items/{item_name}')
def give_item_name(item_name: int):
    return {"item": item_name}


@app.get('/enum/example/{modalName}')
def enum_example(modal_name: EnumClass):
    if modal_name is EnumClass.alexnet:
        return {"modalName": modal_name}
    elif modal_name is EnumClass.resnet:
        return {"modalName": modal_name}
    elif modal_name.value == 'lenet':
        return {"modalName": modal_name}
