from sqlalchemy import ForeignKey, String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, Optional

from .base import Base

if TYPE_CHECKING:
    from .job_post import JobPost


class SummarizedJob(Base):
    __tablename__ = "summarized_job"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    job_post_id: Mapped[int] = mapped_column(
        ForeignKey("job_post.id"), nullable=False, unique=True
    )
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    technical_skills: Mapped[str] = mapped_column(
        Text, nullable=False
    )  # JSON string of skills list
    seniority_level: Mapped[str] = mapped_column(
        String, nullable=False
    )  # e.g., "Junior", "Mid", "Senior", "Staff", "Principal"
    estimated_salary_min: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    estimated_salary_max: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Relationship
    job_post: Mapped["JobPost"] = relationship("JobPost", backref="summary")

    def __repr__(self) -> str:
        return f"SummarizedJob(id={self.id}, job_post_id={self.job_post_id}, seniority_level={self.seniority_level!r})"
