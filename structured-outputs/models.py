from pydantic import BaseModel


class ParticipantEntry(BaseModel):
    name: str
    model_config = {"extra": "forbid"}


class CalenderEvent(BaseModel):
    event_name: str
    venue: str
    date: str
    participants: list[ParticipantEntry]
    model_config = {"extra": "forbid"}
