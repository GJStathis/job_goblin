from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from src.hoarder.models import JobPage
from src.hoarder.repositories import JobPageRepository


class JobPageService:
    """
    Service layer for job page business logic.

    This service centralizes all job page operations, ensuring consistency
    across different application interfaces (CLI, API, Chrome extension).
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.job_page_repo = JobPageRepository(session)

    async def create_job_page(self, url: str, page_html: str) -> JobPage:
        """
        Create a new job page entry.

        Args:
            url: The URL of the job page
            page_html: The HTML content of the page

        Returns:
            The created JobPage object
        """
        job_page = await self.job_page_repo.create(url=url, page_html=page_html)
        return job_page

    async def get_job_page_by_id(self, page_id: int) -> Optional[JobPage]:
        """
        Get a job page by ID.

        Args:
            page_id: The ID of the job page

        Returns:
            JobPage object if found, None otherwise
        """
        return await self.job_page_repo.get_by_id(page_id)

    async def get_job_page_by_url(self, url: str) -> Optional[JobPage]:
        """
        Get a job page by URL.

        Args:
            url: The URL to search for

        Returns:
            JobPage object if found, None otherwise
        """
        return await self.job_page_repo.get_by_url(url)

    async def get_all_job_pages(self) -> list[JobPage]:
        """
        Get all job pages.

        Returns:
            List of all JobPage objects
        """
        return await self.job_page_repo.get_all()

    async def update_job_page(
        self,
        page_id: int,
        url: Optional[str] = None,
        page_html: Optional[str] = None,
    ) -> Optional[JobPage]:
        """
        Update a job page.

        Args:
            page_id: The ID of the job page to update
            url: Optional new URL
            page_html: Optional new HTML content

        Returns:
            Updated JobPage object if found, None otherwise
        """
        return await self.job_page_repo.update(page_id, url, page_html)

    async def delete_job_page(self, page_id: int) -> bool:
        """
        Delete a job page by ID.

        Args:
            page_id: The ID of the job page to delete

        Returns:
            True if deleted, False if not found
        """
        return await self.job_page_repo.delete(page_id)
