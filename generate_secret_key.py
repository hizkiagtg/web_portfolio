#!/usr/bin/env python3
"""
Simple script to generate a Django secret key for production.
Run this script and copy the output to your Vercel environment variables.
"""

import secrets
import string

def get_random_secret_key():
    """
    Generate a random secret key similar to Django's get_random_secret_key.
    """
    chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(chars) for _ in range(50))

if __name__ == "__main__":
    secret_key = get_random_secret_key()
    print("=" * 60)
    print("Django Secret Key Generated:")
    print("=" * 60)
    print(secret_key)
    print("=" * 60)
    print("Copy this key and add it to your Vercel environment variables as:")
    print("SECRET_KEY=" + secret_key)
    print("=" * 60)