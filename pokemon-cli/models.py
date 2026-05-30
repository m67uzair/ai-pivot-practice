from pydantic import BaseModel


class Ability(BaseModel):
    name: str
    url: str


class AbilityEntry(BaseModel):
    ability: Ability
    is_hidden: bool


class Pokemon(BaseModel):
    abilities: list[AbilityEntry]
    name: str
    height: int
    weight: int
