from typing import List, Optional
from datetime import date
from pydantic import BaseModel, Field

class PlaceBase(BaseModel):
    external_id: str
    notes: Optional[str] = None

class PlaceCreate(PlaceBase):
    pass

class PlaceRead(PlaceBase):
    id: int
    visited: bool

    class Config:
        orm_mode = True

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None

class ProjectCreate(ProjectBase):
    places: Optional[List[PlaceCreate]] = Field(default_factory=list, max_items=10)

class ProjectUpdate(ProjectBase):
    pass

class ProjectRead(ProjectBase):
    id: int
    completed: bool
    places: List[PlaceRead] = []

    class Config:
        orm_mode = True
