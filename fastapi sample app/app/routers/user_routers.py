from fastapi import APIRouter, Body, Depends, FastAPI, HTTPException, status
from database import get_all_users, insert_user, get_role, get_user_by_email, get_user_by_username, update_user, get_user_by_id, get_credentials, update_password
from models.models import UserLoginSchema, User, UserUpdate, PasswordUpdate
from internal.auth_bearer import JWTBearer
from internal.auth_handler import signJWT, decodeJWT
from pydantic import ValidationError
from decouple import config
from minio import Minio
from minio.error import S3Error
import bcrypt

HOST = config("MINIO_HOST")
ACCESS_KEY = config("MINIO_ACCESS_KEY")
SECRET_ACCESS_KEY = config("MINIO_SECRET_ACCESS_KEY")
SECURE = config("MINIO_SECURE")

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

## GET URL FROM IMG NAME 
@router.get("/", tags=["users"])
async def read_users():
    print("Get all users")
    users = get_all_users()
    for user in users:
        if user.profile_picture:
            bucket_name = 'profile-pictures'
            object_name = user.profile_picture
            url = get_minio_object_url(bucket_name, object_name)
            print(url)
            if url:
                print(f'URL for {object_name}: {url}')
                user.profile_picture = url
            else:
                print('Failed to retrieve URL.')
                user.profile_picture = get_minio_object_url(bucket_name, "profile-default.png")
    return users

@router.get("/user-by-id/{userid}")
async def user_by_id(userid):
    print("Get user by id")
    user = get_user_by_id(userid)
    print (user)
    return user

# @router.get("/me", dependencies=[Depends(JWTBearer())], tags=["users"])
@router.get("/me", dependencies=[Depends(JWTBearer())], tags=["users"])
async def read_user_me(token: str = Depends(JWTBearer())):
    print("Get current logged in user")
    user_data = decodeJWT(token)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or expired token",
        )
    user = get_user_by_email(user_data.get("user_id"))
    if user['profile_picture']:
        bucket_name = 'profile-pictures'
        object_name = user['profile_picture']
        url = get_minio_object_url(bucket_name, object_name)
        print(url)
        if url:
            print(f'URL for {object_name}: {url}')
            user['profile_picture'] = url
        else:
            print('Failed to retrieve URL.')
            user['profile_picture'] = get_minio_object_url(bucket_name, "profile-default.png")
    return user
# @TODO: na men ferni piso to password, na men ferni disabled users. (en prepi na gini aparetita dame)

@router.get("/{username}", tags=["users"])
async def read_user(username: str):
    print("Get User by username")
    user = get_user_by_username(username)
    if user['profile_picture']:
        bucket_name = 'profile-pictures'
        object_name = user['profile_picture']
        url = get_minio_object_url(bucket_name, object_name)
        print(url)
        if url:
            print(f'URL for {object_name}: {url}')
            user['profile_picture'] = url
        else:
            print('Failed to retrieve URL.')
            user['profile_picture'] = get_minio_object_url(bucket_name, "profile-default.png")
    return user

@router.put("/{user_id}", response_model=UserUpdate, dependencies=[Depends(JWTBearer())], tags=["users"], responses={403: {"description": "Operation forbidden"}})
async def change_user(user: UserUpdate = Body(...)):
    print("Updating User")
    existing_user = get_user_by_id(user.id)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user.id} not found")
    
    print(user.profile_picture)
    update_user(user)
    return user

@router.put("/change-password", response_model=User, dependencies=[Depends(JWTBearer())], tags=["users"], responses={403: {"description": "Operation forbidden"}})
async def change_password(user: PasswordUpdate = Body(...)):
    print("Change password")
    existing_user = get_credentials(user.id)
    print (existing_user)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user.id} not found")
    if existing_user.password != user.current_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Passwords don't match")
    print ("here")
    # update_password(user)
    return user



@router.post("/signup", tags=["user"])
def create_user(user: User = Body(...)):
    print("Sign Up")
    print(user)
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
    print("Login")
    try:
        if check_user(user):
            token = signJWT(user.email)
            return token_response(token)
        else:
            raise HTTPException(status_code=401, detail="Invalid username or password")
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    
# @router.put("/{item_id}", dependencies=[Depends(JWTBearer())], tags=["events"], responses={403: {"description": "Operation forbidden"}})
# async def update_item(item_id: str):
#     if item_id != "plumbus":
#         raise HTTPException(
#             status_code=403, detail="You can only update the item: plumbus"
#         )
#     return {"item_id": item_id, "name": "The great Plumbus"}
    
def token_response(token: str):
    return {"access_token": token}

# @router.post("/login", tags=["user"])
# def user_login(user: UserLoginSchema = Body(...)):
#     if check_user(user):
#         token = signJWT(user.email)
#         return token_response(token)
#     else:
#         raise HTTPException(status_code=401, detail="Invalid username or password")

def get_minio_object_url(bucket_name, object_name):
    # Initialize Minio client
    print(HOST)
    minio_client = Minio(
        'localhost:9000', # Replace with your MinIO server address
        access_key='VKYsbj4UVQrZVCmGgWVR',
        secret_key='52JXYuhvZTKLoO69VULDvF7t6csfrMLEgTng6Jrd',
        secure=False # Set to True if using HTTPS
    )
    print ("here1")
    try:
        minio_client.stat_object(bucket_name, object_name)
        url = minio_client.presigned_get_object(bucket_name, object_name)
        return url
    except S3Error as e:
        print(f'Error occurred: {e}')
        return None
    