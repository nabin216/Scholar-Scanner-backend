#!/usr/bin/env python3

import os
import sys
import django
from datetime import datetime, timedelta

# Add the project root to Python path
sys.path.append('/d/ScholarshipPortal/scholarship-backend')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarships_api.settings')
django.setup()

from scholarships.models import Scholarship
from users.models import User, SavedScholarship

def create_test_scholarships_with_deadlines():
    """Create test scholarships with different deadline scenarios"""
      # Get or create a test user
    try:
        user = User.objects.first()  # Get the first user
        if not user:
            print("No users found. Please create a user first.")
            return
        print(f"Using user: {user.email}")
    except Exception as e:
        print(f"Error getting user: {e}")
        return
    
    today = datetime.now().date()
    
    # Define scholarships with different deadline scenarios
    test_scholarships = [
        {
            'title': 'Urgent Scholarship - Due Today',
            'provider': 'Emergency Foundation',
            'amount': '5000.00',
            'deadline': today,  # Due today
            'description': 'This scholarship is due today - very urgent!'
        },
        {
            'title': 'Critical Scholarship - Due Tomorrow',
            'provider': 'Tomorrow Foundation',
            'amount': '7500.00',
            'deadline': today + timedelta(days=1),  # Due tomorrow
            'description': 'This scholarship is due tomorrow - apply now!'
        },
        {
            'title': 'Soon Scholarship - 3 Days Left',
            'provider': 'Quick Apply Foundation',
            'amount': '3000.00',
            'deadline': today + timedelta(days=3),  # 3 days left
            'description': 'Only 3 days left to apply for this scholarship'
        },
        {
            'title': 'Week Scholarship - 7 Days Left',
            'provider': 'Weekly Foundation',
            'amount': '6000.00',
            'deadline': today + timedelta(days=7),  # 1 week left
            'description': 'One week remaining to submit your application'
        },
        {
            'title': 'Month Scholarship - 20 Days Left',
            'provider': 'Monthly Foundation',
            'amount': '8000.00',
            'deadline': today + timedelta(days=20),  # 20 days left
            'description': 'Good time remaining - 20 days to prepare application'
        },
        {
            'title': 'Future Scholarship - 45 Days Left',
            'provider': 'Future Foundation',
            'amount': '10000.00',
            'deadline': today + timedelta(days=45),  # 45 days left
            'description': 'Plenty of time remaining - 45 days to apply'
        },
        {
            'title': 'Expired Scholarship - 2 Days Overdue',
            'provider': 'Past Foundation',
            'amount': '4000.00',
            'deadline': today - timedelta(days=2),  # 2 days overdue
            'description': 'This scholarship deadline has passed 2 days ago'
        },
        {
            'title': 'Very Expired Scholarship - 10 Days Overdue',
            'provider': 'Ancient Foundation',
            'amount': '12000.00',
            'deadline': today - timedelta(days=10),  # 10 days overdue
            'description': 'This scholarship deadline passed 10 days ago'
        }
    ]
    
    created_scholarships = []
    
    for scholarship_data in test_scholarships:
        # Create or get scholarship
        scholarship, created = Scholarship.objects.get_or_create(
            title=scholarship_data['title'],
            defaults={
                'provider': scholarship_data['provider'],
                'amount': scholarship_data['amount'],
                'deadline': scholarship_data['deadline'],
                'description': scholarship_data['description'],
                'country_id': 1,  # Assuming country with ID 1 exists
                'application_url': 'https://example.com/apply'
            }
        )
        
        if created:
            print(f"Created scholarship: {scholarship.title}")
            created_scholarships.append(scholarship)
              # Save scholarship for the test user
            saved_scholarship, saved_created = SavedScholarship.objects.get_or_create(
                user=user,
                scholarship=scholarship,
                defaults={}
            )
            
            if saved_created:
                print(f"  → Saved for user: {user.email}")
        else:
            print(f"Scholarship already exists: {scholarship.title}")
    
    print(f"\nCreated {len(created_scholarships)} new scholarships with various deadline scenarios")
    print("These scholarships are now saved for the test user and will demonstrate:")
    print("- Due today (red badge)")
    print("- Due tomorrow (orange badge)")
    print("- Due in 3 days (orange badge)")
    print("- Due in 1 week (yellow badge)")
    print("- Due in 20 days (blue badge)")
    print("- Due in 45 days (green badge)")
    print("- Expired 2 days ago (red badge)")
    print("- Expired 10 days ago (red badge)")

if __name__ == "__main__":
    create_test_scholarships_with_deadlines()
