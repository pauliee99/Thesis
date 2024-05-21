from fastapi import APIRouter, Depends, HTTPException, status, Body, BackgroundTasks
from database import get_all_userevents, get_current_userevents, insert_user_event, get_event_users, delete_user_event
from internal.auth_bearer import JWTBearer, get_current_user_role
from internal.auth_handler import decodeJWT
from models.models import UserEvents, EmailSchema
from internal.mailer import send_mail

router = APIRouter(
    prefix="/userevents",
    tags=["userevents"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", dependencies=[Depends(JWTBearer())], tags=["userevents"])
async def read_items():
    return get_all_userevents()


@router.get("/{item_id}", dependencies=[Depends(JWTBearer())], tags=["userevents"])
async def read_item(item_id: int):
    event = get_current_userevents(item_id)
    if not event:
        raise HTTPException(status_code=404, detail="Item not found")
    return event

@router.get("/{item_id}", dependencies=[Depends(JWTBearer())], tags=["userevents"])
async def read_event_users(item_id: int):
    event = get_event_users(item_id)
    if not event:
        raise HTTPException(status_code=404, detail="Item not found")
    return event

@router.post("/", dependencies=[Depends(JWTBearer())], tags=["userevents"])
async def create_userevent(userevent_data: UserEvents = Body(...)):
    insert_user_event(userevent_data)
    return {"message": "Event created successfully", "event": userevent_data}

@router.delete("/{event_id}", dependencies=[Depends(JWTBearer())], tags=["userevents"])
async def delete_event(event_id: int):
    response = delete_user_event(event_id)
    return response

@router.post("/send-email")
def schedule_mail(req: EmailSchema, tasks: BackgroundTasks):
    data = req.dict()
    tasks.add_task(send_mail, data)
    return {"status": 200, "message": "email has been scheduled"}