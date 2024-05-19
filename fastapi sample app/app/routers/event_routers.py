from fastapi import APIRouter, Depends, HTTPException, status
from database import get_all_events, insert_event, get_event_by_id, delete_event_by_id
from internal.auth_bearer import JWTBearer, get_current_user_role
from internal.auth_handler import decodeJWT

router = APIRouter(
    prefix="/events",
    tags=["events"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", dependencies=[Depends(JWTBearer())], tags=["events"])
async def read_items():
    return get_all_events()


@router.get("/{item_id}", dependencies=[Depends(JWTBearer())], tags=["events"])
async def read_item(item_id: str):
    event = get_event_by_id(item_id)
    if not event:
        raise HTTPException(status_code=404, detail="Item not found")
    return event

@router.put(
    "/{item_id}",
    dependencies=[Depends(JWTBearer())],
    tags=["events"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}

@router.post("/", dependencies=[Depends(JWTBearer())], tags=["events"])
async def create_item(event_data: dict, current_user_role: str = Depends(get_current_user_role)):
    print("role here: ", current_user_role.role)
    if current_user_role.role != "Admin" and current_user_role.role != "Manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient privileges. Only admins can create events.",
        )
    insert_event(event_data)
    return {"message": "Event created successfully", "event": event_data}

@router.delete("/{event_id}", dependencies=[Depends(JWTBearer())], tags=["events"])
async def delete_event(event_id: int):
    response = delete_event_by_id(event_id)
    return response

