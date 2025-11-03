#!/usr/bin/env python3
"""
Test script for AI job summarization.

Usage:
    python test/scripts/test_ai_summarization.py <job_id>
    python test/scripts/test_ai_summarization.py 123

This script tests the AIService by:
1. Taking a job_post_id as input
2. Calling AIService.summarize_job()
3. Displaying the results
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.hoarder.utils.database import get_session
from src.hoarder.services.ai_service import AIService
from src.hoarder.repositories import JobPostRepository


def test_ai_summarization(job_id: int) -> None:
    """Test AI summarization for a given job post ID."""
    print(f"\n{'=' * 60}")
    print(f"Testing AI Summarization for Job Post ID: {job_id}")
    print(f"{'=' * 60}\n")

    # Check for API keys
    provider = os.getenv("LLM_PROVIDER", "openai")
    print(f"Using LLM Provider: {provider}\n")

    if provider == "openai" and not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("Please set OPENAI_API_KEY in your .env file")
        return

    if provider == "anthropic" and not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: ANTHROPIC_API_KEY not found in environment variables")
        print("Please set ANTHROPIC_API_KEY in your .env file")
        return

    session = get_session()
    try:
        # 1. Verify job exists
        job_post_repo = JobPostRepository(session)
        job_post = job_post_repo.get_by_id(job_id)

        if not job_post:
            print(f"❌ Error: Job post with ID {job_id} not found")
            return

        print(f"✓ Found job post:")
        print(f"   - Title: {job_post.title}")
        print(f"   - Company: {job_post.company.name}")
        print(f"   - Description length: {len(job_post.description)} characters\n")

        # 2. Call AIService
        print("Calling AIService.summarize_job()...")
        print("(This may take a few seconds...)\n")

        ai_service = AIService(session, provider=provider)
        summarized_job = ai_service.summarize_job(job_id)

        if not summarized_job:
            print("❌ Error: Failed to summarize job post")
            return

        # 3. Display results
        print(f"{'=' * 60}")
        print("✓ Summarization Complete!")
        print(f"{'=' * 60}\n")

        print(f"Summary ID: {summarized_job.id}")
        print(f"\n📝 Summary:")
        print(f"   {summarized_job.summary}\n")

        print(f"💼 Seniority Level:")
        print(f"   {summarized_job.seniority_level}\n")

        print(f"🛠️  Technical Skills:")
        import json

        skills = json.loads(summarized_job.technical_skills)
        for skill in skills:
            print(f"   • {skill}")

        print(f"\n💰 Estimated Salary Range:")
        if summarized_job.estimated_salary_min and summarized_job.estimated_salary_max:
            print(
                f"   ${summarized_job.estimated_salary_min:,} - ${summarized_job.estimated_salary_max:,}"
            )
        else:
            print("   Not specified")

        print(f"\n{'=' * 60}")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
    finally:
        session.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test/scripts/test_ai_summarization.py <job_id>")
        print("Example: python test/scripts/test_ai_summarization.py 123")
        sys.exit(1)

    try:
        job_id = int(sys.argv[1])
    except ValueError:
        print(f"Error: '{sys.argv[1]}' is not a valid integer")
        sys.exit(1)

    test_ai_summarization(job_id)
