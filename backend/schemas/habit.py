import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class HabitCreate(BaseModel):
    name: str
    frequency: str


class HabitRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    frequency: str
    created_at: datetime.datetime


class HabitUpdate(BaseModel):
    name: Optional[str] = None
    frequency: Optional[str] = None


class HabitCompletionCreate(BaseModel):
    logged_at: datetime.date


class HabitCompletionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    habit_id: int
    logged_at: datetime.date
