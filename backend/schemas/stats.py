from pydantic import BaseModel


class SummaryResponse(BaseModel):
    completions: int
    missed: int
    longest_streak: int


class StreakResponse(BaseModel):
    habit_id: int
    name: str
    streak_length: int
