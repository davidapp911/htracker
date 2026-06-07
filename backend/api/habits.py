from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.api.deps import current_user, database_session
from backend.models.user import User
from backend.schemas.habit import (
    HabitCompletionCreate,
    HabitCompletionRead,
    HabitCreate,
    HabitRead,
    HabitUpdate,
)
from backend.services.habits import (
    add_completion,
    create_habit,
    delete_completion,
    delete_habit,
    list_completions,
    read_habit,
    read_habits,
    update_habit,
)
from backend.services.streak import calculate_current_streak

router = APIRouter()


@router.post("/", response_model=HabitRead, status_code=201)
def create(
    body: HabitCreate, db: Session = Depends(database_session), user: User = Depends(current_user)
):
    return create_habit(db, user.id, body)


@router.get("/", response_model=list[HabitRead], status_code=200)
def list_habits(db: Session = Depends(database_session), user: User = Depends(current_user)):
    return read_habits(db, user.id)


@router.get("/{habit_id}", response_model=HabitRead, status_code=200)
def get(habit_id: int, db: Session = Depends(database_session), user: User = Depends(current_user)):
    try:
        habit = read_habit(db, user.id, habit_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return habit


@router.put("/{habit_id}", response_model=HabitRead, status_code=200)
def update(
    habit_id: int,
    body: HabitUpdate,
    db: Session = Depends(database_session),
    user: User = Depends(current_user),
):
    try:
        habit = update_habit(db, user.id, habit_id, body)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return habit


@router.delete("/{habit_id}", response_model=None, status_code=204)
def delete(
    habit_id: int, db: Session = Depends(database_session), user: User = Depends(current_user)
):
    try:
        delete_habit(db, user.id, habit_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{habit_id}/streak", response_model=int, status_code=200)
def get_streak(
    habit_id: int, db: Session = Depends(database_session), user: User = Depends(current_user)
):
    try:
        streak_length = calculate_current_streak(db, user.id, habit_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return streak_length


@router.get("/{habit_id}/logs", response_model=list[HabitCompletionRead], status_code=200)
def get_completions(
    habit_id: int, db: Session = Depends(database_session), user: User = Depends(current_user)
):
    try:
        completions = list_completions(db, user.id, habit_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return completions


@router.post("/{habit_id}/logs", response_model=HabitCompletionRead, status_code=201)
def add_habit_completion(
    body: HabitCompletionCreate,
    habit_id: int,
    db: Session = Depends(database_session),
    user: User = Depends(current_user),
):
    try:
        completion = add_completion(db, user.id, habit_id, body)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return completion


@router.delete("/{habit_id}/logs/{completion_id}", response_model=None, status_code=204)
def delete_habit_completion(
    habit_id: int,
    completion_id: int,
    db: Session = Depends(database_session),
    user: User = Depends(current_user),
):
    try:
        delete_completion(db, user.id, habit_id, completion_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
