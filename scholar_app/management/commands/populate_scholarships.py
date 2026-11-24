"""
Django management command to populate the database with 100+ scholarships
"""

from django.core.management.base import BaseCommand
from scholar_app.models import Scholarship
from django.utils import timezone
from datetime import timedelta
import random


class Command(BaseCommand):
    help = 'Populates the database with 100+ sample scholarships'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting to create scholarships...'))
        
        # Scholarship data templates (Indian context)
        countries = ['India', 'India', 'India', 'India', 'India', 'USA', 'UK', 'Canada', 'Australia', 'Germany', 'France', 'Singapore', 'Japan', 'Netherlands', 'Sweden', 'Switzerland', 'New Zealand', 'Ireland', 'South Korea', 'Norway', 'Denmark']
        
        types = ['Merit-based', 'Need-based', 'Athletic', 'Research', 'Community Service', 'Leadership']
        
        fields = ['Computer Science', 'Engineering', 'Business', 'Medicine', 'Law', 'Arts', 'Science', 'Mathematics', 'Physics', 'Chemistry', 'Biology', 'Economics', 'Psychology', 'Education', 'Environmental Science', 'Social Sciences', 'Humanities', 'Data Science', 'Artificial Intelligence', 'Nursing']
        
        degree_levels = ['Undergraduate', 'Masters', 'PhD', 'Diploma']
        
        providers = [
            'National Education Foundation India',
            'Government of India Scholarship Board',
            'Indian Council of Higher Education',
            'Central Scholarship Scheme',
            'Ministry of Education India',
            'AICTE Scholarship Program',
            'UGC India',
            'MHRD Scholarship Trust',
            'State Government Education Fund',
            'Indian Institute Foundation',
            'National Merit Scholarship Council',
            'All India Education Trust',
            'Indian Technical Education Board',
            'National Research Foundation',
            'Indian Medical Council Scholarship',
            'Engineering Council of India',
            'Indian Business Leaders Network',
            'Science & Technology Ministry India',
            'Minority Education Trust India',
            'SC/ST/OBC Welfare Fund'
        ]
        
        scholarship_templates = [
            {
                'title_template': '{adjective} {field} Scholarship',
                'adjectives': ['Excellence', 'Merit', 'Distinguished', 'Outstanding', 'Premier', 'Elite', 'Advanced', 'International', 'Global', 'Future Leaders']
            },
            {
                'title_template': '{country} {field} Award',
                'adjectives': []
            },
            {
                'title_template': '{provider} {type} Grant',
                'adjectives': []
            },
            {
                'title_template': '{field} Research Fellowship',
                'adjectives': []
            },
            {
                'title_template': 'Future {field} Scholars Program',
                'adjectives': []
            }
        ]
        
        # Clear existing scholarships (optional)
        # Scholarship.objects.all().delete()
        
        scholarships_created = 0
        
        # Generate 120 scholarships
        for i in range(120):
            # Randomly select attributes
            country = random.choice(countries)
            scholarship_type = random.choice(types)
            field = random.choice(fields)
            degree_level = random.choice(degree_levels)
            provider = random.choice(providers)
            
            # Generate title
            template = random.choice(scholarship_templates)
            if template['adjectives']:
                title = template['title_template'].format(
                    adjective=random.choice(template['adjectives']),
                    field=field,
                    country=country,
                    provider=provider,
                    type=scholarship_type
                )
            else:
                title = template['title_template'].format(
                    field=field,
                    country=country,
                    provider=provider,
                    type=scholarship_type
                )
            
            # Generate amount (in INR - Indian Rupees)
            # Typical Indian scholarship amounts: 25,000 to 5,00,000 INR
            amount = random.choice([25000, 50000, 75000, 100000, 150000, 200000, 250000, 300000, 400000, 500000])
            
            # Generate deadline (between 30 and 365 days from now)
            days_ahead = random.randint(30, 365)
            deadline = timezone.now().date() + timedelta(days=days_ahead)
            
            # Generate GPA requirement
            gpa_required = round(random.uniform(2.5, 3.8), 1)
            
            # Generate description
            descriptions = [
                f"This prestigious scholarship supports outstanding {degree_level} students pursuing {field}. Recipients demonstrate exceptional academic achievement and leadership potential.",
                f"The {title} provides financial assistance to talented students in {field}. This award recognizes academic excellence and commitment to the field.",
                f"Designed for high-achieving {degree_level} students, this scholarship supports those pursuing careers in {field}. Applicants should demonstrate strong academic performance and passion for their studies.",
                f"This competitive scholarship is awarded to exceptional students studying {field} at the {degree_level} level. Recipients are selected based on academic merit and potential impact in their field.",
                f"Supporting the next generation of {field} professionals, this scholarship provides significant financial aid to {degree_level} students demonstrating outstanding academic achievement.",
                f"The {provider} is proud to offer this scholarship to talented students pursuing {field}. This award recognizes both academic excellence and leadership qualities.",
                f"This scholarship opportunity is available to {degree_level} students specializing in {field}. Recipients are chosen for their academic achievements and dedication to their field of study.",
                f"Aimed at fostering excellence in {field}, this scholarship supports promising {degree_level} students who show exceptional academic performance and future potential.",
            ]
            
            description = random.choice(descriptions)
            
            # Generate eligibility
            eligibility_templates = [
                f"• Must be enrolled in a {degree_level} program in {field}\n• Minimum GPA of {gpa_required}\n• Strong academic record\n• Demonstrated leadership or community involvement\n• Financial need may be considered",
                f"• Currently pursuing {degree_level} degree in {field}\n• GPA requirement: {gpa_required} or higher\n• Citizenship or permanent residency in {country}\n• Full-time student status\n• Submit personal statement and recommendation letters",
                f"• Accepted or enrolled in {degree_level} program\n• Field of study: {field}\n• Minimum GPA: {gpa_required}\n• Leadership experience preferred\n• Essay submission required",
                f"• {degree_level} student in {field}\n• Academic GPA of {gpa_required}+\n• Demonstrates academic excellence\n• Strong recommendation letters\n• Financial need documentation",
            ]
            
            eligibility = random.choice(eligibility_templates)
            
            # Map degree level
            degree_map = {
                'Undergraduate': 'UG',
                'Masters': 'PG',
                'PhD': 'PHD',
                'Diploma': 'UG'
            }
            degree_code = degree_map.get(degree_level, 'UG')
            
            # Map scholarship type
            type_map = {
                'Merit-based': 'merit',
                'Need-based': 'need',
                'Athletic': 'sports',
                'Research': 'research',
                'Community Service': 'community',
                'Leadership': 'academic'
            }
            type_code = type_map.get(scholarship_type, 'merit')
            
            # Create scholarship
            try:
                scholarship = Scholarship.objects.create(
                    title=title,
                    provider=provider,
                    description=description,
                    amount=amount,
                    deadline=deadline,
                    eligibility_criteria=eligibility,
                    country=country,
                    scholarship_type=type_code,
                    field_of_study=field,
                    degree_level=degree_code,
                    min_gpa=gpa_required,
                    status='active',
                    is_featured=random.choice([True, False]) if i < 10 else False  # Feature first 10
                )
                scholarships_created += 1
                
                if scholarships_created % 20 == 0:
                    self.stdout.write(self.style.SUCCESS(f'Created {scholarships_created} scholarships...'))
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating scholarship: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'✅ Successfully created {scholarships_created} scholarships!'))
        self.stdout.write(self.style.SUCCESS(f'Total scholarships in database: {Scholarship.objects.count()}'))
