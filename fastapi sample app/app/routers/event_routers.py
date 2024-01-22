from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_token_header
from database import get_all_events, insert_event, get_event_by_id

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


@router.get("/")
async def read_items():
    return get_all_events()


@router.get("/{item_id}")
async def read_item(item_id: str):
    event = get_event_by_id(item_id)
    if len(event) == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return event

@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}

@router.post("/")
async def create_item(event_data: dict):
    insert_event(event_data)
    return {"message": "Event created successfully", "event": event_data.dict()}