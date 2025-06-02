#!/usr/bin/env python
"""
Clear Django cache to reset rate limiting counters.
Run this script to clear rate limiting when you hit 429 errors during development.
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarships_api.settings')
django.setup()

from django.core.cache import cache

def clear_rate_limit_cache():
    """Clear all rate limiting cache entries"""
    try:
        # Clear all cache entries
        cache.clear()
        print("✅ Successfully cleared Django cache (including rate limiting data)")
        print("Rate limiting counters have been reset.")
        
        # Also try to clear specific throttling keys if we can identify them
        from django.core.cache.utils import make_template_fragment_key
        
        print("🔄 Cache cleared. You can now make fresh API requests.")
        
    except Exception as e:
        print(f"❌ Error clearing cache: {e}")
        print("You may need to restart the Django server manually.")

if __name__ == '__main__':
    print("🧹 Clearing Django cache to reset rate limiting...")
    clear_rate_limit_cache()
