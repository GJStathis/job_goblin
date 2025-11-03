from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, Optional

from .base import Base

if TYPE_CHECKING:
    from .company import Company


class JobPost(Base):
    __tablename__ = "job_post"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationship
    company: Mapped["Company"] = relationship("Company", back_populates="job_posts")

    def __repr__(self) -> str:
        return (
            f"JobPost(id={self.id}, company_id={self.company_id}, title={self.title!r})"
        )
