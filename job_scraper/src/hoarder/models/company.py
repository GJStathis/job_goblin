from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .job_post import JobPost


class Company(Base):
    __tablename__ = "company"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    industry: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Relationship
    job_posts: Mapped[list["JobPost"]] = relationship(
        "JobPost", back_populates="company"
    )

    def __repr__(self) -> str:
        return f"Company(id={self.id}, name={self.name!r}, industry={self.industry!r})"
