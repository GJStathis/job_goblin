from fastapi import APIRouter, HTTPException, Depends
from src.hoarder.utils.database import get_async_session
from src.hoarder.schema.job_collection import (
    JobPageRequest,
    JobPageResponse,
    JobPageListResponse,
    JobPageItem
)
from src.hoarder.services.job_page_service import JobPageService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/job-collection")


@router.post("/page", response_model=JobPageResponse)
async def create_job_page(
    request: JobPageRequest,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Create a new job page entry in the database.

    Args:
        request: JobPageRequest containing url and page_html

    Returns:
        JobPageResponse with the created page_id and confirmation
    """
    try:
        job_page_service = JobPageService(session)
        job_page = await job_page_service.create_job_page(
            url=request.url,
            page_html=request.page_html
        )

        return JobPageResponse(
            page_id=job_page.page_id,
            url=job_page.url,
            message="Job page saved successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving job page: {str(e)}")


@router.get("/page/{page_id}", response_model=JobPageResponse)
async def get_job_page(
    page_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get a job page by ID.

    Args:
        page_id: The ID of the job page to retrieve

    Returns:
        JobPageResponse with the job page details
    """
    try:
        job_page_service = JobPageService(session)
        job_page = await job_page_service.get_job_page_by_id(page_id)

        if not job_page:
            raise HTTPException(status_code=404, detail=f"Job page with ID {page_id} not found")

        return JobPageResponse(
            page_id=job_page.page_id,
            url=job_page.url,
            message="Job page retrieved successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving job page: {str(e)}")


@router.get("/pages", response_model=JobPageListResponse)
async def get_all_job_pages(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get all job pages.

    Returns:
        JobPageListResponse with list of all job pages and total count
    """
    try:
        job_page_service = JobPageService(session)
        job_pages = await job_page_service.get_all_job_pages()

        return JobPageListResponse(
            total=len(job_pages),
            pages=[
                JobPageItem(page_id=page.page_id, url=page.url)
                for page in job_pages
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving job pages: {str(e)}")