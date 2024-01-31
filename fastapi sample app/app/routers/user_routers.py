from fastapi import APIRouter
from database import get_all_users

router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users():
    return get_all_users()


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}