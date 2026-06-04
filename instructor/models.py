from pydantic import BaseModel


class CareerStep(BaseModel):
    title: str
    detail: str
    model_config = {"extra": "forbid"}


class CareerAdvice(BaseModel):
    summary: str
    steps: list[CareerStep]
    timeline_months: int
    model_config = {"extra": "forbid"}
