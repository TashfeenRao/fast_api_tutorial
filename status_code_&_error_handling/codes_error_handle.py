import uvicorn
from fastapi import FastAPI, status, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()


class Tags:
    default = "hello world"
    user = "user"


class CustomExceptionHandle(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(CustomExceptionHandle)
async def handle_custom_exception(request: Request, exe: CustomExceptionHandle):
    return JSONResponse(
        status_code=405,
        content={
            "message": f"ops we found {exe.name} that cause us to break the process"
        },
    )


class UserBase(BaseModel):
    name: str


@app.get("/", status_code=status.HTTP_200_OK, tags=[Tags.default])
def hello_world():
    return "hello world"


@app.post(
    "/save/user",
    status_code=status.HTTP_201_CREATED,
    tags=[Tags.user],
    summary="Endpoint to save user",
)
def save_user(user_id: int):
    """
    :param user_id:
    :return: user_id
    This endpoint has been created to save the user in the Db. It has one restriction for those user
    that has already been created in Db and for those who have been blocked by the management
    """
    if user_id == 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This id has blocked!",
            headers={"token": "secret"},
        )
    elif user_id == 4:
        raise CustomExceptionHandle(name="bug")
    return user_id


if __name__ == "__main__":
    uvicorn.run("codes_error_handle:app", host="localhost", port=8000, reload=True)
