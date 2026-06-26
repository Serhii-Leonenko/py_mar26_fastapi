import datetime
import enum

from sqlalchemy import Table, Column, ForeignKey, String, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class TaskStatus(str, enum.Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    DONE = "done"


task_assignees = Table(
    "task_assignees",
    Base.metadata,
    Column("task_id", ForeignKey("tasks.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
        default=TaskStatus.NEW,
        nullable=False,
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )
    project: Mapped["Project"] = relationship(back_populates="tasks")

    assignees: Mapped[list["User"]] = relationship(
        secondary=task_assignees,
        back_populates="assigned_tasks",
    )

    __table_args__ = (
        UniqueConstraint("title", "project_id", name="unique_task_title_per_project"),
    )
