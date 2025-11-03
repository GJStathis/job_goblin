import json
import os
from typing import Optional, Union
from sqlalchemy.orm import Session
from langchain_openai import ChatOpenAI  # type: ignore[import-untyped]
from langchain_anthropic import ChatAnthropic  # type: ignore[import-untyped]
from langchain_core.messages import HumanMessage, SystemMessage  # type: ignore[import-untyped]
from dotenv import load_dotenv

from src.hoarder.models import SummarizedJob
from src.hoarder.repositories import JobPostRepository, SummarizedJobRepository

# Load environment variables
load_dotenv()


class AIService:
    """
    Service for AI-powered job analysis using LangChain.

    Supports OpenAI and Anthropic models for job summarization.
    """

    def __init__(self, job_post_repo: JobPostRepository, summarized_job_repo: SummarizedJobRepository, provider: str = "openai"):
        """
        Initialize AIService with a database session.

        Args:
            session: SQLAlchemy session
            provider: LLM provider - "openai" or "anthropic" (default: openai)
        """
        self.job_post_repo = job_post_repo
        self.summarized_job_repo = summarized_job_repo

        # Initialize LLM based on provider
        if provider == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
            self.llm: Union[ChatAnthropic, ChatOpenAI] = ChatAnthropic(
                model="claude-3-5-sonnet-20241022",
                api_key=api_key,  # type: ignore[call-arg,arg-type]
            )
        else:  # default to openai
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            self.llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)  # type: ignore[call-arg,arg-type]

    def summarize_job(self, job_post_id: int) -> Optional[SummarizedJob]:
        """
        Summarize a job posting using an LLM.

        Retrieves the job post, sends it to an LLM for analysis, and stores
        the summary in the summarized_job table.

        Args:
            job_post_id: ID of the job post to summarize

        Returns:
            SummarizedJob object if successful, None if job not found
        """
        # 1. Get the job post
        job_post = self.job_post_repo.get_by_id(job_post_id)
        if not job_post:
            print(f"Job post {job_post_id} not found")
            return None

        # Check if already summarized
        existing_summary = self.summarized_job_repo.get_by_job_post_id(job_post_id)
        if existing_summary:
            print(f"Job post {job_post_id} already has a summary")
            return existing_summary

        # 2. Build prompt for LLM
        system_prompt = """You are an expert job analyst. Analyze the following job posting and provide:

1. A concise summary (2-3 sentences)
2. A list of technical skills required (as a JSON array)
3. The seniority level (one of: "Entry", "Junior", "Mid", "Senior", "Staff", "Principal", "Lead")
4. An estimated salary range in USD (min and max as integers)

Return your response as a JSON object with these exact keys:
{
    "summary": "string",
    "technical_skills": ["skill1", "skill2", ...],
    "seniority_level": "string",
    "estimated_salary_min": integer or null,
    "estimated_salary_max": integer or null
}"""

        user_prompt = f"""Job Title: {job_post.title}

Job Description:
{job_post.description}

Company: {job_post.company.name if job_post.company else "Unknown"}
"""

        try:
            # 3. Call LLM
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt),
            ]

            response = self.llm.invoke(messages)  # type: ignore[attr-defined]
            response_text = response.content

            # 4. Parse LLM response
            # Try to extract JSON from the response
            # Ensure response_text is a string
            if isinstance(response_text, list):
                response_text = str(response_text)

            if "```json" in response_text:
                # Extract JSON from markdown code block
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                json_str = response_text[start:end].strip()
            else:
                json_str = response_text.strip()

            result = json.loads(json_str)

            # 5. Save to database
            summarized_job = self.summarized_job_repo.create(
                job_post_id=job_post_id,
                summary=result["summary"],
                technical_skills=json.dumps(result["technical_skills"]),
                seniority_level=result["seniority_level"],
                estimated_salary_min=result.get("estimated_salary_min"),
                estimated_salary_max=result.get("estimated_salary_max"),
            )

            print(f"✓ Successfully summarized job post {job_post_id}")
            return summarized_job

        except json.JSONDecodeError as e:
            print(f"Error parsing LLM response: {e}")
            print(f"Response was: {response_text}")
            return None

        except Exception as e:
            print(f"Error summarizing job post {job_post_id}: {e}")
            return None
