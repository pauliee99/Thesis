from fastapi import APIRouter, Depends, HTTPException, status, Body, BackgroundTasks
from database import get_all_userevents, get_current_userevents, insert_user_event, get_event_users, delete_user_event, get_user_by_id, get_user_event_record
from internal.auth_bearer import JWTBearer, get_current_user_role
from internal.auth_handler import decodeJWT
from models.models import UserEvents, EmailSchema, User
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

@router.get("/event/{item_id}", dependencies=[Depends(JWTBearer())], tags=["userevents"])
async def read_event_users(item_id: int):
    event = get_event_users(item_id)
    if not event:
        raise HTTPException(status_code=404, detail="Item not found")
    return event

@router.get("/{user_id}/{event_id}", dependencies=[Depends(JWTBearer())], tags=["userevents"])
async def read_user_event(user_id: int, event_id: int):
    record = get_user_event_record(user_id, event_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@router.post("/", dependencies=[Depends(JWTBearer())], tags=["userevents"])
async def create_userevent(userevent_data: UserEvents = Body(...)):
    insert_user_event(userevent_data)
    user = get_user_by_id(userevent_data.user)
    email_data = {
            "email": [user['email']], 
            "subject": "New User Event Created",
            "body": f"Dear {user['firstname']} {user['lastname']}, <br> You just joined in a new event"  # @TODO: add a better email template
        }
    send_mail(email_data)
    return {"message": "Event created successfully", "event": userevent_data}

@router.delete("/", dependencies=[Depends(JWTBearer())], tags=["userevents"])
async def delete_event(userevent_data: UserEvents = Body(...)):
    response = delete_user_event(userevent_data)
    return response

@router.post("/send-email")
def schedule_mail(req: EmailSchema, tasks: BackgroundTasks):
    data = req.dict()
    tasks.add_task(send_mail, data)
    return {"status": 200, "message": "email has been scheduled"}