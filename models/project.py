import datetime

from sqlalchemy import String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    owner: Mapped["User"] = relationship(back_populates="projects")

    tasks: Mapped[list["Task"]] = relationship(back_populates="project")
