from fastapi import APIRouter, Body, Depends, FastAPI, HTTPException
from database import get_all_users, insert_user, get_role
from models.models import UserLoginSchema, User
from internal.auth_bearer import JWTBearer
from internal.auth_handler import signJWT
from pydantic import ValidationError

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

def check_user(data: UserLoginSchema):
    users = get_all_users()
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False

@router.get("/", tags=["users"])
async def read_users():
    return get_all_users()


@router.get("/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}

@router.post("/signup", tags=["user"])
def create_user(user: User = Body(...)):
    print(user)
    insert_user(user) # replace with db call, making sure to hash the password first
    return signJWT(user.email)

# @router.post("/login", tags=["user"])
# def user_login(user: UserLoginSchema = Body(...)):
#     if check_user(user):
#         return signJWT(user.email)
#     return {
#         "error": "Wrong login details!"
#     }

@router.post("/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(...)):
    try:
        if check_user(user):
            token = signJWT(user.email, get_role(user.email).role)
            return token_response(token)
        else:
            raise HTTPException(status_code=401, detail="Invalid username or password")
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    
def token_response(token: str):
    return {"access_token": token}

# @router.post("/login", tags=["user"])
# def user_login(user: UserLoginSchema = Body(...)):
#     if check_user(user):
#         token = signJWT(user.email)
#         return token_response(token)
#     else:
#         raise HTTPException(status_code=401, detail="Invalid username or password")