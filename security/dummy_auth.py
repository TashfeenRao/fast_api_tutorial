from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uvicorn
from pydantic import BaseModel, EmailStr

app = FastAPI()


auth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


class User(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    disabled: bool


class UserInDB(User):
    hashed_password: str


def hash_password(password: str):
    return "fakehashed" + password


def get_user_from_db(db, username):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user is not in our system"
        )


def decode_token(token: str):
    user = get_user_from_db(fake_users_db, token)
    return user


def get_current_user(token: str = Depends(auth2_scheme)):
    user = decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
        )
    return user


def get_current_user_active(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="This user has been blocked"
        )
    return current_user


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db[form_data.username]
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    user = UserInDB(**user_dict)
    hashed_password = hash_password(form_data.password)
    if user.hashed_password != hashed_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/current/user")
def get_user(current_user: User = Depends(get_current_user_active)):
    return current_user


@app.get("/")
def hello_world(token: str = Depends(auth2_scheme)):
    return "hello world"


if __name__ == "__main__":
    uvicorn.run("dummy_auth:app", host="localhost", port=8000, reload=True)
