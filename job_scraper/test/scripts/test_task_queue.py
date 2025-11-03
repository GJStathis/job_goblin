#!/usr/bin/env python3
"""
Test queuing a task to verify Celery can receive and process it.
"""

from src.hoarder.tasks.job_processing import process_job_post_task


def test_queue_task():
    """Test queueing a task"""
    print("Testing task queueing...")
    print("=" * 50)

    try:
        print("\n1. Checking registered tasks...")
        from src.hoarder.celery_app import celery_app

        registered_tasks = list(celery_app.tasks.keys())
        print(f"   Found {len(registered_tasks)} registered tasks:")
        for task in registered_tasks:
            if not task.startswith("celery."):
                print(f"   - {task}")

        print("\n2. Queueing test task...")
        # Queue a task for job post ID 1
        result = process_job_post_task.delay(1)
        print(f"   ✓ Task queued with ID: {result.id}")
        print(f"   Task name: {process_job_post_task.name}")

        print("\n3. Checking task status...")
        print(f"   State: {result.state}")

        print("\n" + "=" * 50)
        print("✓ Task queued successfully!")
        print("=" * 50)
        print("\nCheck your Celery worker logs to see the task being processed.")
        print("You should see:")
        print("  [INFO/MainProcess] Task process_job_post[...] received")
        print("  Processing job post ID: 1")

        return True

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_queue_task()
