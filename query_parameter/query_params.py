from enum import Enum
import uvicorn
from fastapi import FastAPI, Query

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class UserEnum(str, Enum):
    tashi = "software engineer"
    umair = "team lead"


app = FastAPI()

# fastapi know which is path parameter which is query parameter
# query params here is optional if not provided than fastapi don't mind that
@app.get("/items/{item_id}")
def query_params_defaults(item_id: str, limit: int = 0):
    if limit:
        return {limit: limit}
    return {item_id: item_id}


# we can required the query params by not providing the default values
# fast api will automatically convert the type if possible
# yes,on,true, True,1 any uppercase of the str consider as true opposite will be fasle
@app.get("/item/{item_id}/user/{user_id}")
def query_required_params(item_id: int, user_id: int, short: bool):
    if short:
        return {item_id: item_id, user_id: user_id, "boolean": short}
    else:
        return {item_id: item_id, user_id: user_id}


# we can use enum class for query parms that will allow us to only accept defined values for query
@app.get("/ricult")
def enum_query_params(team_member: UserEnum):
    return {"team_member": team_member, "team_member_value": team_member.value}


# we can fastApi built in func Query() for extra validation we need for query param
# we can use min/max/alias/regex for validating the incoming param
# we can meta data information too in Query()
# we can also use default key to initialize the param if we want to required the param we just don't include default key
# Example regex is only accept admin string as query param
@app.get("/usertype/")
def get_user_type(
    user_type: str = Query(
        min_length=3,
        max_length=15,
        regex="^admin$",
        title="Get User Type",
        description="This endpoint will get usertype from user",
    )
):
    return user_type


if __name__ == "__main__":
    uvicorn.run(
        "query_params:app",
        host="localhost",
        port=8000,
        reload=True,
        debug=True,
        workers=3,
    )
