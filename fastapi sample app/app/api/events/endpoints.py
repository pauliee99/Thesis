from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.api.events import crud, models

router = APIRouter()

@router.get("/", response_model=list[models.Event])
def read_events(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    events = crud.get_events(db, skip=skip, limit=limit)
    return events

@router.post("/", response_model=models.Event)
def create_event(event: models.EventCreate, db: Session = Depends(get_db)):
    return crud.create_event(db=db, event=event)
