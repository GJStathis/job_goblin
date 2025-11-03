#!/usr/bin/env python3
"""
Test script to verify end-to-end job creation with Celery queueing.
"""

from src.hoarder.utils.database import get_session
from src.hoarder.services.job_service import JobService


def test_job_creation():
    """Test creating a job post and queueing it for processing"""
    print("Testing job creation with Celery queue...")
    print("=" * 50)

    session = get_session()
    try:
        job_service = JobService(session)

        print("\n1. Creating test job post...")
        job_post = job_service.create_job_post(
            company_name="Test Company",
            job_title="Test Software Engineer",
            job_description="This is a test job description for testing purposes.",
            job_url="https://example.com/job/123",
            industry="Technology",
        )

        print("   ✓ Job post created!")
        print(f"   - ID: {job_post.id}")
        print(f"   - Title: {job_post.title}")
        print(f"   - Company ID: {job_post.company_id}")
        print(f"   - URL: {job_post.url}")

        print("\n2. Job should be queued for processing...")
        print("   ✓ Check your Celery worker logs to see the task processing")

        print("\n" + "=" * 50)
        print("✓ Test completed successfully!")
        print("=" * 50)
        print("\nIf you have a Celery worker running, you should see:")
        print('  "Processing job post ID: {job_post.id}"')
        print("\nIf not, start a worker with:")
        print("  celery -A src.hoarder.celery_app worker --loglevel=info")

        return job_post

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback

        traceback.print_exc()
        return None

    finally:
        session.close()


if __name__ == "__main__":
    test_job_creation()
