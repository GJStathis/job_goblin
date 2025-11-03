#!/usr/bin/env python3
"""
Test script to verify Celery and Redis integration.
"""

import sys
from redis.exceptions import ConnectionError
from src.hoarder.tasks.job_processing import process_job_post_task


def test_celery_connection():
    """Test Celery connection to Redis"""
    print("Testing Celery configuration...")
    print("-" * 50)

    try:
        # Import Celery app
        print("1. Importing Celery app...")
        from src.hoarder.celery_app import celery_app

        print("   ✓ Celery app imported successfully")

        # Test connection to broker
        print("\n2. Testing broker connection (Redis)...")
        result = celery_app.control.inspect().active()
        if result is None:
            print("   ⚠ No workers are currently running")
            print("   (This is OK if you haven't started a worker yet)")
        else:
            print(f"   ✓ Connected to broker. Active workers: {len(result)}")

        # Test broker URL
        print("\n3. Checking broker configuration...")
        print(f"   Broker URL: {celery_app.conf.broker_url}")
        print(f"   Backend URL: {celery_app.conf.result_backend}")

        # Try to ping Redis directly
        print("\n4. Testing direct Redis connection...")
        import redis

        r = redis.from_url(celery_app.conf.broker_url, decode_responses=True)
        r.ping()
        print("   ✓ Redis connection successful")

        print("\n" + "=" * 50)
        print("✓ Celery configuration is correct!")
        print("=" * 50)
        print("\nTo start a worker, run:")
        print("  celery -A src.hoarder.celery_app worker --loglevel=info")

        print("\n 5. Test sending job to celery worker")
        process_job_post_task.delay(2)

    except ConnectionError as e:
        print(f"\n✗ Redis Connection Error: {e}")
        print("\n⚠ Redis is not running or not accessible")
        print("\nStart Redis with:")
        print("  redis-server")
        print("\nOr as a service:")
        print("  brew services start redis")
        return False

    except ImportError as e:
        print(f"\n✗ Import Error: {e}")
        print("\nMake sure all dependencies are installed:")
        print("  uv sync")
        return False

    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback

        traceback.print_exc()
        return False


def test_task_import():
    """Test importing Celery tasks"""
    print("\n" + "=" * 50)
    print("Testing task imports...")
    print("-" * 50)

    try:
        print("1. Importing job processing task...")
        from src.hoarder.tasks.job_processing import process_job_post_task

        print("   ✓ Tasks imported successfully")
        print(f"   Task name: {process_job_post_task.name}")

        print("\n✓ All task imports successful!")
        return True

    except Exception as e:
        print(f"\n✗ Error importing tasks: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_celery_connection()
    if success:
        test_task_import()
    else:
        sys.exit(1)
