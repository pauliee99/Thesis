from fastapi import APIRouter, Body, Depends, FastAPI, HTTPException, status
from database import get_all_users, insert_user, get_role, get_user_by_email, get_user_by_username
from models.models import UserLoginSchema, User
from internal.auth_bearer import JWTBearer
from internal.auth_handler import signJWT, decodeJWT
from pydantic import ValidationError
import bcrypt

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

def check_user(data: UserLoginSchema):
    users = get_all_users()
    for user in users:
        print (user)
        if user.email == data.email and bcrypt.checkpw(data.password.encode('utf-8'), user.password.encode('utf-8')):
            return True
    return False

@router.get("/", tags=["users"])
async def read_users():
    return get_all_users()


# @router.get("/me", dependencies=[Depends(JWTBearer())], tags=["users"])
@router.get("/me", dependencies=[Depends(JWTBearer())], tags=["users"])
async def read_user_me(token: str = Depends(JWTBearer())):
    user_data = decodeJWT(token)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or expired token",
        )
    return get_user_by_email(user_data.get("user_id"))
# @TODO: na men ferni piso to password, na men ferni disabled users. (en prepi na gini aparetita dame)


@router.get("/{username}", tags=["users"])
async def read_user(username: str):
    user = get_user_by_username(username)
    print(user)
    return user

@router.post("/signup", tags=["user"])
def create_user(user: User = Body(...)):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    user.password = hashed_password.decode('utf-8')
    insert_user(user)
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
            token = signJWT(user.email)
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