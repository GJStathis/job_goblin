#!/usr/bin/env python3
"""
Test script to verify Redis connection.
Run this to diagnose Redis connectivity issues.
"""

import redis
from redis.exceptions import ConnectionError


def test_redis_connection():
    """Test connection to Redis server"""
    print("Testing Redis connection...")
    print("-" * 50)

    try:
        # Connect to Redis
        r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

        # Test 1: Ping
        print("1. Testing PING...")
        response = r.ping()
        print(f"   ✓ PING response: {response}")

        # Test 2: Set a value
        print("\n2. Testing SET...")
        r.set("test_key", "test_value")
        print("   ✓ Successfully set test_key")

        # Test 3: Get the value
        print("\n3. Testing GET...")
        value = r.get("test_key")
        print(f"   ✓ Retrieved value: {value}")

        # Test 4: Delete the key
        print("\n4. Testing DEL...")
        r.delete("test_key")
        print("   ✓ Successfully deleted test_key")

        # Test 5: Check server info
        print("\n5. Checking Redis server info...")
        info = r.info("server")
        print(f"   ✓ Redis version: {info['redis_version']}")
        print(f"   ✓ OS: {info['os']}")
        print(f"   ✓ Uptime (seconds): {info['uptime_in_seconds']}")

        print("\n" + "=" * 50)
        print("✓ All Redis tests passed!")
        print("=" * 50)
        return True

    except ConnectionError as e:
        print(f"\n✗ Connection Error: {e}")
        print("\nPossible solutions:")
        print("1. Make sure Redis is installed:")
        print("   brew install redis")
        print("\n2. Start Redis server:")
        print("   redis-server")
        print("\n3. Or start Redis as a service:")
        print("   brew services start redis")
        return False

    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return False


if __name__ == "__main__":
    test_redis_connection()
