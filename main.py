import uvicorn
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def hello_world():
    return {"message": "Hello World new changes"}


@app.get("/item")
async def hello_world():
    return {"message": "Hello World new changes"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="localhost", port=8000, reload=True, debug=True, workers=3
    )
