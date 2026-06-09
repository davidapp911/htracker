from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.habit import Habit, HabitCompletion
from backend.schemas.habit import HabitCompletionCreate, HabitCreate, HabitUpdate


def create_habit(db: Session, user_id: int, data: HabitCreate) -> Habit:
    habit = Habit(name=data.name, frequency=data.frequency, user_id=user_id)
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit


def read_habits(db: Session, user_id: int) -> list[Habit]:
    habits = db.execute(select(Habit).where(Habit.user_id == user_id)).scalars().all()

    return list(habits)


def read_habit(db: Session, user_id: int, habit_id: int) -> Habit:
    habit = db.execute(
        select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id)
    ).scalar_one_or_none()

    if not habit:
        raise ValueError("Habit not found")

    return habit


def update_habit(db: Session, user_id: int, habit_id: int, data: HabitUpdate) -> Habit:
    habit = read_habit(db, user_id, habit_id)
    update_data = data.model_dump(exclude_unset=True)

    for attribute, value in update_data.items():
        setattr(habit, attribute, value)

    db.commit()
    db.refresh(habit)

    return habit


def delete_habit(db: Session, user_id: int, habit_id: int) -> None:
    habit = read_habit(db, user_id, habit_id)

    db.delete(habit)
    db.commit()


def add_completion(
    db: Session, user_id: int, habit_id: int, data: HabitCompletionCreate
) -> HabitCompletion:
    read_habit(db, user_id, habit_id)
    existing = db.execute(
        select(HabitCompletion).where(
            HabitCompletion.habit_id == habit_id, HabitCompletion.logged_at == data.logged_at
        )
    )

    if existing:
        raise ValueError("Already completed")

    completion = HabitCompletion(logged_at=data.logged_at, habit_id=habit_id)

    db.add(completion)
    db.commit()
    db.refresh(completion)

    return completion


def find_completion(
    db: Session, user_id: int, habit_id: int, completion_id: int
) -> HabitCompletion:
    read_habit(db, user_id, habit_id)

    completion = db.execute(
        select(HabitCompletion).where(
            HabitCompletion.id == completion_id,
            HabitCompletion.habit_id == habit_id,
        )
    ).scalar_one_or_none()

    if not completion:
        raise ValueError("Completion not found")

    return completion


def list_completions(db: Session, user_id: int, habit_id: int) -> list[HabitCompletion]:
    read_habit(db, user_id, habit_id)

    completions = (
        db.execute(select(HabitCompletion).where(HabitCompletion.habit_id == habit_id))
        .scalars()
        .all()
    )

    return list(completions)


def delete_completion(db: Session, user_id: int, habit_id: int, completion_id: int) -> None:
    completion = find_completion(db, user_id, habit_id, completion_id)

    db.delete(completion)
    db.commit()
