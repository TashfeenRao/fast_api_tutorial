from fastapi import FastAPI, Cookie, Header
import uvicorn


app = FastAPI()


@app.get('/')
def hello_world():
    return {"hello": "world"}

# we can use same extra validation when we use Cookie() from fastapi
@app.get('/save/cookie')
async def save_cookie(cookie_id: str = Cookie(default=None)):
    print(cookie_id)
    return {"cookie": cookie_id}


@app.get('/get/header')
def get_header(user_agent: str | None = Header(default=None)):
    return {"header": user_agent}

if __name__ == '__main__':
    uvicorn.run('cookie_header:app', port=8000, host='localhost', reload=True)