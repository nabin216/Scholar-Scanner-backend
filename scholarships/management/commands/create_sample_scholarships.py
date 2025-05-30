from django.core.management.base import BaseCommand
from scholarships.models import (
    Scholarship, Country, Level, ScholarshipCategory, 
    FieldOfStudy, FundType, SponsorType
)
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Create sample scholarships for testing'

    def handle(self, *args, **options):
        # Create countries if they don't exist
        usa, _ = Country.objects.get_or_create(name='United States')
        canada, _ = Country.objects.get_or_create(name='Canada')
        uk, _ = Country.objects.get_or_create(name='United Kingdom')
        
        # Create levels
        undergraduate, _ = Level.objects.get_or_create(name='Undergraduate')
        graduate, _ = Level.objects.get_or_create(name='Graduate')
        postgraduate, _ = Level.objects.get_or_create(name='Postgraduate')
        
        # Create categories
        merit, _ = ScholarshipCategory.objects.get_or_create(name='Merit-based')
        need, _ = ScholarshipCategory.objects.get_or_create(name='Need-based')
        research, _ = ScholarshipCategory.objects.get_or_create(name='Research')
        
        # Create fields of study
        engineering, _ = FieldOfStudy.objects.get_or_create(name='Engineering')
        medicine, _ = FieldOfStudy.objects.get_or_create(name='Medicine')
        business, _ = FieldOfStudy.objects.get_or_create(name='Business')
        computer_science, _ = FieldOfStudy.objects.get_or_create(name='Computer Science')
        
        # Create fund types
        full_funding, _ = FundType.objects.get_or_create(name='Full Funding')
        partial_funding, _ = FundType.objects.get_or_create(name='Partial Funding')
        
        # Create sponsor types
        government, _ = SponsorType.objects.get_or_create(name='Government')
        private, _ = SponsorType.objects.get_or_create(name='Private Foundation')
        university, _ = SponsorType.objects.get_or_create(name='University')
        
        # Create sample scholarships
        scholarships_data = [
            {
                'title': 'Excellence in Engineering Scholarship',
                'description': 'A prestigious scholarship for outstanding engineering students.',
                'provider': 'Global Tech Foundation',
                'amount': 15000.00,
                'country': usa,
                'deadline': date.today() + timedelta(days=120),
                'levels': [undergraduate, graduate],
                'categories': [merit],
                'fields': [engineering, computer_science],
                'fund_types': [partial_funding],
                'sponsors': [private],
            },
            {
                'title': 'Medical Research Grant',
                'description': 'Supporting future medical professionals and researchers.',
                'provider': 'Health Sciences Institute',
                'amount': 25000.00,
                'country': canada,
                'deadline': date.today() + timedelta(days=90),
                'levels': [graduate, postgraduate],
                'categories': [research, merit],
                'fields': [medicine],
                'fund_types': [full_funding],
                'sponsors': [government, university],
            },
            {
                'title': 'Business Leadership Award',
                'description': 'For students demonstrating exceptional leadership in business.',
                'provider': 'Corporate Excellence Foundation',
                'amount': 10000.00,
                'country': uk,
                'deadline': date.today() + timedelta(days=60),
                'levels': [undergraduate],
                'categories': [merit],
                'fields': [business],
                'fund_types': [partial_funding],
                'sponsors': [private],
            },
            {
                'title': 'Community Service Scholarship',
                'description': 'Recognizing students who make a difference in their communities.',
                'provider': 'Civic Engagement Alliance',
                'amount': 5000.00,
                'country': usa,
                'deadline': date.today() + timedelta(days=45),
                'levels': [undergraduate, graduate],
                'categories': [merit],
                'fields': [engineering, business, medicine],
                'fund_types': [partial_funding],
                'sponsors': [private],
            },
            {
                'title': 'STEM Innovation Grant',
                'description': 'Supporting innovative research in Science, Technology, Engineering, and Mathematics.',
                'provider': 'National Science Foundation',
                'amount': 20000.00,
                'country': usa,
                'deadline': date.today() + timedelta(days=180),
                'levels': [graduate, postgraduate],
                'categories': [research],
                'fields': [engineering, computer_science],
                'fund_types': [full_funding],
                'sponsors': [government],
            }
        ]
        
        created_count = 0
        for data in scholarships_data:
            scholarship, created = Scholarship.objects.get_or_create(
                title=data['title'],
                defaults={
                    'description': data['description'],
                    'provider': data['provider'],
                    'amount': data['amount'],
                    'country': data['country'],
                    'deadline': data['deadline'],
                    'application_url': f'https://example.com/apply/{data["title"].lower().replace(" ", "-")}',
                    'is_featured': created_count < 2,  # Make first 2 featured
                }
            )
            
            if created:
                # Add many-to-many relationships
                scholarship.levels.set(data['levels'])
                scholarship.scholarship_category.set(data['categories'])
                scholarship.field_of_study.set(data['fields'])
                scholarship.fund_type.set(data['fund_types'])
                scholarship.sponsor_type.set(data['sponsors'])
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created scholarship: {scholarship.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Scholarship already exists: {scholarship.title}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} scholarships')
        )
