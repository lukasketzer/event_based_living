
from fastapi import FastAPI, HTTPException, Path, Body
from typing import List, Optional
from ..event_service.db_utils import SessionLocal
from ..event_service.repository import EventsDB
from ..event_service.models import Event, EventOptional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# List all events
@app.get("/events", response_model=List[EventOptional])
def read_events():
    db = SessionLocal()
    events = db.query(EventsDB).limit(50).all()
    db.close()
    return events

# Get a single event by ID
@app.get("/events/{event_id}", response_model=EventOptional)
def get_event(event_id: str = Path(...)):
    db = SessionLocal()
    event = db.query(EventsDB).filter(EventsDB.id == event_id).first()
    db.close()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event



