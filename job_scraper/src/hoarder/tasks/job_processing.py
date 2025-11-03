import os
from src.hoarder.celery_app import celery_app
from src.hoarder.utils.database import get_session
from src.hoarder.repositories import JobPostRepository
from src.hoarder.services.ai_service import AIService


@celery_app.task(name="process_job_post", bind=True)
def process_job_post_task(self, job_post_id: int) -> dict[str, str]:
    """
    Celery task to process a job post for LLM summarization.

    This task:
    1. Retrieves the job post from the database
    2. Uses AIService to generate a summary via LLM
    3. Stores the summary in the summarized_job table

    Args:
        job_post_id: The ID of the JobPost to process

    Returns:
        dict with status and message
    """
    session = get_session()
    try:
        job_post_repo = JobPostRepository(session)
        job_post = job_post_repo.get_by_id(job_post_id)

        if not job_post:
            return {
                "status": "error",
                "message": f"JobPost with ID {job_post_id} not found",
            }

        print(f"Processing job post ID: {job_post_id}")
        print(f"Title: {job_post.title}")
        print(f"Company ID: {job_post.company_id}")
        print(f"Description length: {len(job_post.description)} characters")

        # Check if AI processing is enabled
        provider = os.getenv("LLM_PROVIDER", "openai")  # openai or anthropic
        api_key = (
            os.getenv("OPENAI_API_KEY")
            if provider == "openai"
            else os.getenv("ANTHROPIC_API_KEY")
        )

        if not api_key:
            print(f"⚠ No {provider.upper()} API key found - skipping AI summarization")
            return {
                "status": "skipped",
                "message": "AI summarization skipped - no API key configured",
            }

        # Use AIService to summarize the job
        ai_service = AIService(session, provider=provider)
        summarized_job = ai_service.summarize_job(job_post_id)

        if summarized_job:
            return {
                "status": "success",
                "message": f"Successfully summarized job post {job_post_id}",
            }
        else:
            return {
                "status": "error",
                "message": f"Failed to summarize job post {job_post_id}",
            }

    except Exception as e:
        print(f"Error processing job post {job_post_id}: {e}")
        return {
            "status": "error",
            "message": f"Error processing job post: {str(e)}",
        }

    finally:
        session.close()
