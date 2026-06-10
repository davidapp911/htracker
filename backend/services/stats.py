import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.models.habit import Habit, HabitCompletion
from backend.schemas.stats import StatsResponse, StreakResponse
from backend.services.habits import read_habits
from backend.services.streak import calculate_current_streak


def get_all_streaks(db: Session, user_id: int) -> list[StreakResponse]:
    habits = read_habits(db, user_id)

    return [
        StreakResponse(
            habit_id=h.id,
            name=h.name,
            streak_length=calculate_current_streak(db, user_id, h.id, datetime.date.today()),
        )
        for h in habits
    ]


def get_stats(db: Session, user_id: int, days: int) -> StatsResponse:
    cutoff = datetime.date.today() - datetime.timedelta(days=days - 1)

    completions = (
        db.execute(
            select(func.count())
            .select_from(HabitCompletion)
            .join(Habit)
            .where(Habit.user_id == user_id, HabitCompletion.logged_at >= cutoff)
        ).scalar()
        or 0
    )

    habit_count = (
        db.execute(select(func.count()).select_from(Habit).where(Habit.user_id == user_id)).scalar()
        or 0
    )

    missed = (habit_count * days) - completions

    streaks = get_all_streaks(db, user_id)

    longest_streak = max((s.streak_length for s in streaks), default=0)

    return StatsResponse(completions=completions, missed=missed, longest_streak=longest_streak)
