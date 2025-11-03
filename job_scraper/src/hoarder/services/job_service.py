from typing import Optional
from sqlalchemy.orm import Session

from src.hoarder.models import JobPost
from src.hoarder.repositories import CompanyRepository, JobPostRepository
from src.hoarder.tasks.job_processing import process_job_post_task


class JobService:
    """
    Service layer for job posting business logic.

    This service centralizes all job posting operations, ensuring consistency
    across different application interfaces (CLI, Streamlit, API).
    """

    def __init__(self, company_repo: CompanyRepository, job_post_repo: JobPostRepository):
        self.company_repo = company_repo
        self.job_post_repo = job_post_repo

    def create_job_post(
        self,
        company_name: str,
        job_title: str,
        job_description: str,
        job_url: Optional[str] = None,
        industry: Optional[str] = None,
    ) -> JobPost:
        """
        Create a new job posting with all related operations.

        This method:
        1. Gets or creates the company
        2. Creates the job post in the database
        3. Queues the job post for LLM processing via Celery

        Args:
            company_name: Name of the company
            job_title: Title of the job posting
            job_description: Full job description
            job_url: Optional URL to the job posting
            industry: Optional industry classification

        Returns:
            The created JobPost object
        """
        # 1. Get or create company
        company = self.company_repo.get_or_create(name=company_name, industry=industry)

        # 2. Create job post in database
        job_post = self.job_post_repo.create(
            company_id=company.id,
            title=job_title,
            description=job_description,
            url=job_url,
        )

        # 3. Queue job post for processing (summarization, extraction, etc.)
        try:
            process_job_post_task.delay(job_post.id)
        except Exception as e:
            # Log the error but don't fail the job creation
            # The job is already saved, queue failure shouldn't break the flow
            print(
                f"Warning: Failed to queue job post {job_post.id} for processing: {e}"
            )

        return job_post

    def get_job_post_by_id(self, job_post_id: int) -> Optional[JobPost]:
        """Get a job post by ID"""
        return self.job_post_repo.get_by_id(job_post_id)

    def get_all_job_posts(self) -> list[JobPost]:
        """Get all job posts"""
        return self.job_post_repo.get_all()

    def get_job_posts_by_company(self, company_id: int) -> list[JobPost]:
        """Get all job posts for a specific company"""
        return self.job_post_repo.get_by_company_id(company_id)
