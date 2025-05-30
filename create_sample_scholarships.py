#!/usr/bin/env python
import os
import sys
import django
from datetime import date, timedelta

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarships_api.settings')
django.setup()

from scholarships.models import (
    Scholarship, Country, Level, ScholarshipCategory, 
    FieldOfStudy, FundType, SponsorType
)

def create_sample_data():
    print("Creating sample scholarship data...")
    
    # Create or get countries
    usa, _ = Country.objects.get_or_create(name="United States")
    canada, _ = Country.objects.get_or_create(name="Canada")
    uk, _ = Country.objects.get_or_create(name="United Kingdom")
    
    # Create or get levels
    undergraduate, _ = Level.objects.get_or_create(name="Undergraduate")
    graduate, _ = Level.objects.get_or_create(name="Graduate")
    phd, _ = Level.objects.get_or_create(name="PhD")
    
    # Create or get categories
    merit, _ = ScholarshipCategory.objects.get_or_create(name="Merit-based")
    need, _ = ScholarshipCategory.objects.get_or_create(name="Need-based")
    diversity, _ = ScholarshipCategory.objects.get_or_create(name="Diversity")
    
    # Create or get fields of study
    engineering, _ = FieldOfStudy.objects.get_or_create(name="Engineering")
    medicine, _ = FieldOfStudy.objects.get_or_create(name="Medicine")
    business, _ = FieldOfStudy.objects.get_or_create(name="Business")
    arts, _ = FieldOfStudy.objects.get_or_create(name="Arts")
    
    # Create or get fund types
    full_tuition, _ = FundType.objects.get_or_create(name="Full Tuition")
    partial_tuition, _ = FundType.objects.get_or_create(name="Partial Tuition")
    living_expenses, _ = FundType.objects.get_or_create(name="Living Expenses")
    
    # Create or get sponsor types
    university, _ = SponsorType.objects.get_or_create(name="University")
    government, _ = SponsorType.objects.get_or_create(name="Government")
    private, _ = SponsorType.objects.get_or_create(name="Private Foundation")
    
    # Create sample scholarships
    scholarships_data = [
        {
            'title': 'Excellence in Engineering Scholarship',
            'provider': 'Tech Innovation Foundation',
            'amount': 15000,
            'description': 'Supporting outstanding students pursuing engineering degrees with demonstrated academic excellence and innovation potential.',
            'country': usa,
            'deadline': date.today() + timedelta(days=90),
            'levels': [undergraduate, graduate],
            'categories': [merit],
            'fields': [engineering],
            'fund_types': [partial_tuition],
            'sponsor_types': [private],
        },
        {
            'title': 'Global Health Initiative Grant',
            'provider': 'World Health Foundation',
            'amount': 25000,
            'description': 'Full funding for medical students committed to global health initiatives and underserved communities.',
            'country': canada,
            'deadline': date.today() + timedelta(days=120),
            'levels': [graduate, phd],
            'categories': [merit, diversity],
            'fields': [medicine],
            'fund_types': [full_tuition, living_expenses],
            'sponsor_types': [private],
        },
        {
            'title': 'Future Business Leaders Scholarship',
            'provider': 'Business Excellence Institute',
            'amount': 8000,
            'description': 'Supporting the next generation of business leaders with entrepreneurial spirit and leadership potential.',
            'country': uk,
            'deadline': date.today() + timedelta(days=60),
            'levels': [undergraduate],
            'categories': [merit],
            'fields': [business],
            'fund_types': [partial_tuition],
            'sponsor_types': [university],
        },
        {
            'title': 'Creative Arts Diversity Fellowship',
            'provider': 'Arts & Culture Alliance',
            'amount': 12000,
            'description': 'Promoting diversity in creative arts through financial support for underrepresented students.',
            'country': usa,
            'deadline': date.today() + timedelta(days=75),
            'levels': [undergraduate, graduate],
            'categories': [diversity, need],
            'fields': [arts],
            'fund_types': [partial_tuition, living_expenses],
            'sponsor_types': [private],
        },
        {
            'title': 'STEM Women Leadership Award',
            'provider': 'Women in STEM Foundation',
            'amount': 20000,
            'description': 'Empowering women in STEM fields through comprehensive financial support and mentorship programs.',
            'country': canada,
            'deadline': date.today() + timedelta(days=100),
            'levels': [graduate, phd],
            'categories': [diversity, merit],
            'fields': [engineering, medicine],
            'fund_types': [full_tuition],
            'sponsor_types': [private],
        }
    ]
    
    created_count = 0
    for data in scholarships_data:
        # Check if scholarship already exists
        existing = Scholarship.objects.filter(title=data['title']).first()
        if existing:
            print(f"Scholarship '{data['title']}' already exists, skipping...")
            continue
            
        # Create scholarship
        scholarship = Scholarship.objects.create(
            title=data['title'],
            provider=data['provider'],
            amount=data['amount'],
            description=data['description'],
            country=data['country'],
            deadline=data['deadline'],
            open_date=date.today(),
            is_featured=created_count < 2,  # Make first 2 featured
        )
        
        # Add many-to-many relationships
        scholarship.levels.set(data['levels'])
        scholarship.scholarship_category.set(data['categories'])
        scholarship.field_of_study.set(data['fields'])
        scholarship.fund_type.set(data['fund_types'])
        scholarship.sponsor_type.set(data['sponsor_types'])
        
        created_count += 1
        print(f"Created scholarship: {scholarship.title}")
    
    print(f"\nSample data creation completed! Created {created_count} new scholarships.")
    print(f"Total scholarships in database: {Scholarship.objects.count()}")

if __name__ == '__main__':
    create_sample_data()
