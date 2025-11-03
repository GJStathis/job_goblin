from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class JobPage(Base):
    __tablename__ = "job_page"

    page_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    page_html: Mapped[str] = mapped_column(Text, nullable=False)

    def __repr__(self) -> str:
        return f"JobPage(page_id={self.page_id}, url={self.url!r})"
