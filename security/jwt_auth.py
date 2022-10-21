from datetime import timedelta, datetime

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
import uvicorn

# to get a string like this run:
# openssl rand -hex 32
from pydantic import EmailStr, BaseModel

SECRET_KEY = "5240d187d1b4f0d3419aca58698e1242568ef8196b28946424a692743bf512ed"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()
auth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"])
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
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


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    disabled: bool


class UserInDB(User):
    hashed_password: str


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(fake_db, username):
    if username in fake_db:
        user_dict = fake_db[username]
        return UserInDB(**user_dict)
    return None


async def get_current_user(token: str = Depends(auth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={"www-Authenticate": "Bearer"},
        detail="could not validate user",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    current_user = get_user(fake_users_db, username)
    if not current_user:
        raise credentials_exception
    return current_user


def get_current_user_active(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="user is blocked"
        )
    return current_user


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expiry):
    copy_data = data.copy()
    if expiry:
        copy_data.update({"exp": expiry + datetime.utcnow()})
    else:
        copy_data.update({"exp": timedelta(minutes=15) + datetime.utcnow()})
    token = jwt.encode(copy_data, SECRET_KEY, algorithm=ALGORITHM)
    return token


@app.get("/", dependencies=[Depends(auth2_scheme)])
def hello_world():
    return "Hello World"


@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    expire_time = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expiry=expire_time)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/user/me", response_model=User)
def check_user_access(current_user: User = Depends(get_current_user_active)):
    return current_user


if __name__ == "__main__":
    uvicorn.run("jwt_auth:app", host="localhost", port=8000, reload=True)
