#!/usr/bin/env python3
"""
Test script to verify the password length validation fix.
"""

import sys
import os

# Add the app directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from app.models.user import UserCreate

def test_password_validation():
    print("Testing password validation...")

    # Test 1: Short password (should raise error)
    try:
        user_short = UserCreate(username="testuser", email="test@example.com", password="short")
        print("❌ ERROR: Short password should have raised an error")
    except ValueError as e:
        print(f"✅ Good: Short password raised error: {e}")

    # Test 2: Normal password (should work fine)
    try:
        user_normal = UserCreate(username="testuser", email="test@example.com", password="normalpassword123")
        print(f"✅ Good: Normal password accepted: {len(user_normal.password.encode('utf-8'))} bytes")
    except Exception as e:
        print(f"❌ ERROR: Normal password should have worked: {e}")

    # Test 3: Long password (should be truncated to 72 bytes)
    long_password = "a" * 80  # 80 bytes
    try:
        user_long = UserCreate(username="testuser", email="test@example.com", password=long_password)
        original_bytes = len(long_password.encode('utf-8'))
        final_bytes = len(user_long.password.encode('utf-8'))
        print(f"✅ Good: Long password truncated from {original_bytes} to {final_bytes} bytes")
        assert final_bytes <= 72, f"Password should be <= 72 bytes, got {final_bytes}"
    except Exception as e:
        print(f"❌ ERROR: Long password should have been truncated: {e}")

    # Test 4: 72-byte password (should work fine)
    # Create a 72-byte password
    password_72_bytes = "a" * 72
    try:
        user_72 = UserCreate(username="testuser", email="test@example.com", password=password_72_bytes)
        final_bytes = len(user_72.password.encode('utf-8'))
        print(f"✅ Good: 72-byte password accepted: {final_bytes} bytes")
        assert final_bytes <= 72, f"Password should be <= 72 bytes, got {final_bytes}"
    except Exception as e:
        print(f"❌ ERROR: 72-byte password should have worked: {e}")

    # Test 5: Multi-byte characters (UTF-8)
    unicode_password = "🚀🔥password" + "a" * 60  # Contains multi-byte UTF-8 characters
    try:
        user_unicode = UserCreate(username="testuser", email="test@example.com", password=unicode_password)
        original_bytes = len(unicode_password.encode('utf-8'))
        final_bytes = len(user_unicode.password.encode('utf-8'))
        print(f"✅ Good: Unicode password handled, truncated from {original_bytes} to {final_bytes} bytes")
        assert final_bytes <= 72, f"Password should be <= 72 bytes, got {final_bytes}"
    except Exception as e:
        print(f"❌ ERROR: Unicode password should have been handled: {e}")

if __name__ == "__main__":
    test_password_validation()
    print("\nAll tests completed!")