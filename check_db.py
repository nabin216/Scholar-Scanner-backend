#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarships_api.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    # Check the structure of the scholarships_scholarship table
    cursor.execute("PRAGMA table_info(scholarships_scholarship);")
    columns = cursor.fetchall()
    
    print("Scholarships table columns:")
    for col in columns:
        print(f"  {col[1]} ({col[2]})")  # name and type
    
    # Check if we have any data
    cursor.execute("SELECT id, title, provider, amount FROM scholarships_scholarship LIMIT 3;")
    rows = cursor.fetchall()
    
    print(f"\nSample data ({len(rows)} rows):")
    for row in rows:
        print(f"  ID: {row[0]}, Title: {row[1][:50]}..., Provider: {row[2]}, Amount: {row[3]}")
