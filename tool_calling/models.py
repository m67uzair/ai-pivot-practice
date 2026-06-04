from pydantic import BaseModel


class GetWeatherArgs(BaseModel):
    latitude: float
    longitude: float

