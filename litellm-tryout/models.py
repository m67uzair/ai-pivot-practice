from pydantic import BaseModel


class CalendarEvent(BaseModel):
    name: str
    date: str
    attendees: list[str]
