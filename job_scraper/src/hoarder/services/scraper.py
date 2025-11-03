import requests
from bs4 import BeautifulSoup
from typing import Optional


class JobData:
    """Data class to hold parsed job information"""

    def __init__(
        self,
        company_name: str,
        job_title: str,
        job_description: str,
        industry: Optional[str] = None,
    ):
        self.company_name = company_name
        self.job_title = job_title
        self.job_description = job_description
        self.industry = industry


def scrape_job_page(url: str) -> Optional[JobData]:
    """
    Scrape a job posting URL and extract job information.

    This is a basic implementation that attempts to parse common job posting patterns.
    You may need to customize this based on the specific websites you're scraping.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        # Basic extraction logic - customize based on target websites
        # This is a placeholder implementation
        company_name = "Unknown Company"
        job_title = "Unknown Title"
        job_description = "No description found"
        industry = None

        # Try to extract title from common patterns
        if soup.find("h1"):
            title_tag = soup.find("h1")
            if title_tag and title_tag.text:
                job_title = title_tag.text.strip()

        # Try to extract company name from meta tags or common patterns
        meta_tag = soup.find("meta", {"property": "og:site_name"})
        if meta_tag and hasattr(meta_tag, "get"):
            content = meta_tag.get("content")
            if content:
                company_name = str(content).strip()

        # Try to extract description
        if soup.find("div", class_=lambda x: x and "description" in x.lower()):
            desc_tag = soup.find(
                "div", class_=lambda x: x and "description" in x.lower()
            )
            if desc_tag and desc_tag.text:
                job_description = desc_tag.text.strip()
        elif soup.find("body"):
            # Fallback to body text
            body = soup.find("body")
            if body:
                job_description = body.get_text(separator="\n", strip=True)[:1000]

        return JobData(
            company_name=company_name,
            job_title=job_title,
            job_description=job_description,
            industry=industry,
        )

    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    except Exception as e:
        print(f"Error parsing page: {e}")
        return None
