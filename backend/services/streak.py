import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.habit import HabitCompletion
from backend.services.habits import read_habit


def calculate_current_streak(
    db: Session, user_id: int, habit_id: int, today: datetime.date | None = None
) -> int:
    read_habit(db, user_id, habit_id)

    if not today:
        today = datetime.date.today()

    yesterday = today - datetime.timedelta(days=1)

    completions = (
        db.execute(
            select(HabitCompletion).where(
                HabitCompletion.habit_id == habit_id, HabitCompletion.logged_at <= today
            )
        )
        .scalars()
        .all()
    )

    descending_order = sorted(list(completions), key=lambda x: x.logged_at, reverse=True)
    streak_length = 0

    if descending_order:
        ref = None

        if descending_order[0].logged_at == today:
            ref = today
        elif descending_order[0].logged_at == yesterday:
            ref = yesterday

        if ref:
            for completion in descending_order:
                diff = int((ref - completion.logged_at).days)

                if diff <= 1:
                    streak_length += 1
                else:
                    break

                ref = completion.logged_at

    return streak_length
