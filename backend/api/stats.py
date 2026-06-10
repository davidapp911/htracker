from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.api.deps import current_user, database_session
from backend.core.exceptions import ServiceError
from backend.models.user import User
from backend.schemas.stats import StatsResponse, StreakResponse
from backend.services.stats import get_all_streaks, get_stats

router = APIRouter()


@router.get("/streaks", response_model=list[StreakResponse])
def get_streaks(db: Session = Depends(database_session), user: User = Depends(current_user)):
    try:
        streaks = get_all_streaks(db, user.id)
    except ServiceError as e:
        raise HTTPException(status_code=e.code, detail=e.message)

    return streaks


@router.get("/summary", response_model=StatsResponse)
def get_summary(
    days: int = 7, db: Session = Depends(database_session), user: User = Depends(current_user)
):
    try:
        stats = get_stats(db, user.id, days)
    except ServiceError as e:
        raise HTTPException(status_code=e.code, detail=e.message)

    return stats
