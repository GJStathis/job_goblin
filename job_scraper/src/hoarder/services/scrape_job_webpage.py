import requests
from typing import Optional
from sqlalchemy.orm import Session

from src.hoarder.models import JobPage
from src.hoarder.repositories import JobPageRepository


def scrape_and_save_job_webpage(url: str, job_page_repo: JobPageRepository) -> Optional[JobPage]:
    """
    Fetch a job webpage and save it to the database.

    Args:
        url: The URL of the job posting to fetch
        session: Database session

    Returns:
        JobPage object if successful, None otherwise
    """
    try:
        # Fetch the webpage
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Get the HTML content
        page_html = response.text

        # Save to database using repository
        job_page = job_page_repo.create(url=url, page_html=page_html)

        return job_page

    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    except Exception as e:
        print(f"Error saving page to database: {e}")
        return None
