from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.db.base import Base

if TYPE_CHECKING:
    from backend.models.user import User


class Habit(Base):
    __tablename__ = "habits"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    frequency: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped[User] = relationship(back_populates="habits")

    completions: Mapped[list[HabitCompletion]] = relationship(back_populates="habit")


class HabitCompletion(Base):
    __tablename__ = "completions"
    __table_args__ = (UniqueConstraint("habit_id", "logged_at"),)
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    logged_at: Mapped[datetime.date] = mapped_column(Date, nullable=False)

    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id", ondelete="CASCADE"))
    habit: Mapped[Habit] = relationship(back_populates="completions")
