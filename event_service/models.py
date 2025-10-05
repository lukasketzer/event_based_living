import datetime
from pydantic import BaseModel, field_validator
from typing import Optional
from .enums import event_types

class Event(BaseModel):
    name: str
    description: str
    event_type: event_types.EventType
    start_date: datetime.date
    start_time: datetime.time
    end_date: datetime.date
    end_time: datetime.time
    address: str
    city: str
    country: str
    postal_code: str
    venue: str
    url: str = ""
    price: str

class EventOptional(Event):
    start_date: datetime.date | None = None
    start_time: datetime.time | None = None
    end_date: datetime.date | None = None
    end_time: datetime.time | None = None
    venue: Optional[str] = None
    price: Optional[str] = None

    @field_validator("start_date", "end_date", mode="before")
    def validate_dates(cls, value):
        if isinstance(value, str):
            try:
                return datetime.datetime.strptime(value, "%d.%m.%Y").date()
            except ValueError:
                return None
        elif isinstance(value, datetime.date):
            return value
        return None

    @field_validator("start_time", "end_time", mode="before")
    def validate_times(cls, value):
        if isinstance(value, str):
            try:
                return datetime.datetime.strptime(value, "%H:%M:%S").time()
            except ValueError:
                try:
                    return datetime.datetime.strptime(value, "%H:%M").time()
                except ValueError:
                    return None
        elif isinstance(value, datetime.time):
            return value
        return None

class ListEventOptional(BaseModel):
    events: list[EventOptional]

class ListEvent(BaseModel):
    events: list[Event]
