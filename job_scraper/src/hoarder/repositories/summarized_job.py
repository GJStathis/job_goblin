from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.hoarder.models import SummarizedJob


class SummarizedJobRepository:
    """Repository for SummarizedJob model operations"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        job_post_id: int,
        summary: str,
        technical_skills: str,
        seniority_level: str,
        estimated_salary_min: Optional[int] = None,
        estimated_salary_max: Optional[int] = None,
    ) -> SummarizedJob:
        """Create a new summarized job"""
        summarized_job = SummarizedJob(
            job_post_id=job_post_id,
            summary=summary,
            technical_skills=technical_skills,
            seniority_level=seniority_level,
            estimated_salary_min=estimated_salary_min,
            estimated_salary_max=estimated_salary_max,
        )
        self.session.add(summarized_job)
        await self.session.commit()
        await self.session.refresh(summarized_job)
        return summarized_job

    async def get_by_id(self, summarized_job_id: int) -> Optional[SummarizedJob]:
        """Get a summarized job by ID"""
        res = await self.session.execute(
            select(SummarizedJob).filter(SummarizedJob.id == summarized_job_id)
        )
        return res.scalar_one_or_none()

    async def get_by_job_post_id(self, job_post_id: int) -> Optional[SummarizedJob]:
        """Get a summarized job by job post ID"""
        res = await self.session.execute(
            select(SummarizedJob).filter(SummarizedJob.job_post_id == job_post_id)
        )
        return res.scalar_one_or_none()

    async def get_all(self) -> list[SummarizedJob]:
        """Get all summarized jobs"""
        res = await self.session.execute(select(SummarizedJob))
        return list(res.scalars().all())

    async def update(
        self,
        summarized_job_id: int,
        summary: Optional[str] = None,
        technical_skills: Optional[str] = None,
        seniority_level: Optional[str] = None,
        estimated_salary_min: Optional[int] = None,
        estimated_salary_max: Optional[int] = None,
    ) -> Optional[SummarizedJob]:
        """Update a summarized job"""
        summarized_job = await self.get_by_id(summarized_job_id)
        if not summarized_job:
            return None

        if summary is not None:
            summarized_job.summary = summary
        if technical_skills is not None:
            summarized_job.technical_skills = technical_skills
        if seniority_level is not None:
            summarized_job.seniority_level = seniority_level
        if estimated_salary_min is not None:
            summarized_job.estimated_salary_min = estimated_salary_min
        if estimated_salary_max is not None:
            summarized_job.estimated_salary_max = estimated_salary_max

        await self.session.commit()
        await self.session.refresh(summarized_job)
        return summarized_job

    async def delete(self, summarized_job_id: int) -> bool:
        """Delete a summarized job by ID"""
        summarized_job = await self.get_by_id(summarized_job_id)
        if not summarized_job:
            return False

        await self.session.delete(summarized_job)
        await self.session.commit()
        return True
