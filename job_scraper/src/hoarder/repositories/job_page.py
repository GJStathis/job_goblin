from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.hoarder.models import JobPage


class JobPageRepository:
    """Repository for JobPage model operations"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, url: str, page_html: str) -> JobPage:
        """Create a new job page"""
        job_page = JobPage(url=url, page_html=page_html)
        self.session.add(job_page)
        await self.session.commit()
        await self.session.refresh(job_page)
        return job_page

    async def get_by_id(self, page_id: int) -> Optional[JobPage]:
        """Get a job page by ID"""
        res = await self.session.execute(select(JobPage).filter(JobPage.page_id == page_id))
        return res.scalar_one_or_none()

    async def get_by_url(self, url: str) -> Optional[JobPage]:
        """Get a job page by URL"""
        res = await self.session.execute(select(JobPage).filter(JobPage.url == url))
        return res.scalar_one_or_none()

    async def get_all(self) -> list[JobPage]:
        """Get all job pages"""
        res = await self.session.execute(select(JobPage))
        return list(res.scalars().all())

    async def update(
        self,
        page_id: int,
        url: Optional[str] = None,
        page_html: Optional[str] = None,
    ) -> Optional[JobPage]:
        """Update a job page"""
        job_page = await self.get_by_id(page_id)
        if not job_page:
            return None

        if url is not None:
            job_page.url = url
        if page_html is not None:
            job_page.page_html = page_html

        await self.session.commit()
        await self.session.refresh(job_page)
        return job_page

    async def delete(self, page_id: int) -> bool:
        """Delete a job page by ID"""
        job_page = await self.get_by_id(page_id)
        if not job_page:
            return False

        await self.session.delete(job_page)
        await self.session.commit()
        return True
