from fastapi import FastAPI, Depends, Header, HTTPException
import uvicorn

# we can also define global dependencies at top
app = FastAPI()


class CommonQuery:
    def __init__(self, q: str = "default"):
        self.q = q


def verify_token(token: str = Header()):
    if token == "not allowed":
        raise HTTPException(status_code=403, detail="This user is blocked")
    return True


def custom_param(q: str | None = None, limit: int | None = None):
    return {q, limit}


@app.get("/")
def hello_world():
    return "Hello World"


@app.get("/item")
def get_item(item_param: dict = Depends(custom_param)):
    """
    we can use custom function which this path operation function depends on that function will execute first
    than it will return some value which we can use in path operation function. This is very power full, it will allow
    us to create dependency to some external resources like db, apis etc
    """
    return f"hello {item_param}"


# dependencies defined in path is only for execution it won't return any thing in return
@app.get(
    "/user",
    dependencies=[Depends(custom_param), Depends(CommonQuery), Depends(verify_token)],
)
def get_user():
    return "get user"


if __name__ == "__main__":
    uvicorn.run("dependency:app", host="localhost", port=8000, reload=True)
