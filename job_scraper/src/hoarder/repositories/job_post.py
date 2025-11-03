from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.hoarder.models import JobPost


class JobPostRepository:
    """Repository for JobPost model operations"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        company_id: int,
        title: str,
        description: str,
        url: Optional[str] = None,
    ) -> JobPost:
        """Create a new job post"""
        job_post = JobPost(
            company_id=company_id, title=title, description=description, url=url
        )
        self.session.add(job_post)
        await self.session.commit()
        await self.session.refresh(job_post)
        return job_post

    async def get_by_id(self, job_post_id: int) -> Optional[JobPost]:
        """Get a job post by ID"""
        res = await self.session.execute(select(JobPost).filter(JobPost.id == job_post_id))
        return res.scalar_one_or_none()

    async def get_all(self) -> list[JobPost]:
        """Get all job posts"""
        res = await self.session.execute(select(JobPost))
        return list(res.scalars().all())

    async def get_by_company_id(self, company_id: int) -> list[JobPost]:
        """Get all job posts for a specific company"""
        res = await self.session.execute(select(JobPost).filter(JobPost.company_id == company_id))
        return list(res.scalars().all())

    async def update(
        self,
        job_post_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        url: Optional[str] = None,
    ) -> Optional[JobPost]:
        """Update a job post"""
        job_post = await self.get_by_id(job_post_id)
        if not job_post:
            return None

        if title is not None:
            job_post.title = title
        if description is not None:
            job_post.description = description
        if url is not None:
            job_post.url = url

        await self.session.commit()
        await self.session.refresh(job_post)
        return job_post

    async def delete(self, job_post_id: int) -> bool:
        """Delete a job post by ID"""
        job_post = await self.get_by_id(job_post_id)
        if not job_post:
            return False

        await self.session.delete(job_post)
        await self.session.commit()
        return True
