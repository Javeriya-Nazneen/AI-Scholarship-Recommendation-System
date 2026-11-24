"""
Django management command to reset and populate scholarships with Indian context
"""

from django.core.management.base import BaseCommand
from scholar_app.models import Scholarship
from django.utils import timezone
from datetime import timedelta
import random


class Command(BaseCommand):
    help = 'Reset and populate database with Indian scholarships'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Deleting existing scholarships...'))
        
        # Delete all existing scholarships
        deleted_count = Scholarship.objects.all().delete()[0]
        self.stdout.write(self.style.SUCCESS(f'Deleted {deleted_count} scholarships'))
        
        self.stdout.write(self.style.SUCCESS('Creating new Indian scholarships...'))
        
        # Indian scholarship data
        indian_states = ['Maharashtra', 'Delhi', 'Karnataka', 'Tamil Nadu', 'West Bengal', 'Gujarat', 'Telangana', 'Uttar Pradesh', 'Rajasthan', 'Kerala']
        
        countries = ['India'] * 70 + ['USA', 'UK', 'Canada', 'Australia', 'Germany', 'France', 'Singapore', 'Japan', 'Netherlands', 'Sweden'] * 5
        
        types = ['Merit-based', 'Need-based', 'Research', 'Community Service', 'Leadership', 'Sports']
        
        fields = [
            'Computer Science', 'Engineering', 'Business', 'Medicine', 'Law', 
            'Arts', 'Science', 'Mathematics', 'Physics', 'Chemistry', 'Biology',
            'Economics', 'Psychology', 'Education', 'Environmental Science',
            'Data Science', 'Artificial Intelligence', 'Nursing', 'Pharmacy', 'Agriculture'
        ]
        
        degree_levels = ['Undergraduate', 'Masters', 'PhD', 'Diploma']
        
        indian_providers = [
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
            'National Research Foundation India',
            'Indian Medical Council Scholarship',
            'Engineering Council of India',
            'Indian Business Leaders Network',
            'Science & Technology Ministry India',
            'Minority Affairs Ministry India',
            'SC/ST/OBC Welfare Department',
            'Central Government Merit Scholarship',
            'Post Matric Scholarship Scheme',
            'National Means-cum-Merit Scholarship',
            'Prime Minister Scholarship Scheme',
            'Chief Minister Scholarship Program',
            'Indian Space Research Organization',
            'Defence Research Development Organisation',
            'Council of Scientific Industrial Research',
            'Indian Council of Medical Research',
            'Department of Biotechnology India'
        ]
        
        scholarship_templates = [
            {
                'title_template': '{adjective} {field} Scholarship',
                'adjectives': ['Excellence', 'Merit', 'Distinguished', 'Outstanding', 'Premier', 'Elite', 'Advanced', 'National', 'All India', 'Central']
            },
            {
                'title_template': '{state} State {field} Award',
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
                'title_template': 'National {field} Scholars Program',
                'adjectives': []
            },
            {
                'title_template': 'All India {field} Excellence Award',
                'adjectives': []
            }
        ]
        
        scholarships_created = 0
        
        # Generate 120 scholarships
        for i in range(120):
            # Randomly select attributes
            country = random.choice(countries)
            scholarship_type = random.choice(types)
            field = random.choice(fields)
            degree_level = random.choice(degree_levels)
            provider = random.choice(indian_providers)
            state = random.choice(indian_states)
            
            # Generate title
            template = random.choice(scholarship_templates)
            if template['adjectives']:
                title = template['title_template'].format(
                    adjective=random.choice(template['adjectives']),
                    field=field,
                    state=state,
                    provider=provider,
                    type=scholarship_type
                )
            else:
                title = template['title_template'].format(
                    field=field,
                    state=state,
                    provider=provider,
                    type=scholarship_type
                )
            
            # Generate amount in INR (Indian Rupees)
            # Typical ranges: 25,000 to 10,00,000 INR
            if country == 'India':
                # Indian scholarships: ₹25K to ₹5L
                amount = random.choice([25000, 50000, 75000, 100000, 150000, 200000, 250000, 300000, 400000, 500000])
            else:
                # International scholarships: ₹5L to ₹50L (higher for foreign studies)
                amount = random.choice([500000, 750000, 1000000, 1500000, 2000000, 2500000, 3000000, 4000000, 5000000])
            
            # Generate deadline (between 30 and 365 days from now)
            days_ahead = random.randint(30, 365)
            deadline = timezone.now().date() + timedelta(days=days_ahead)
            
            # Generate GPA requirement (Indian system: 6.0-10.0 CGPA)
            gpa_required = round(random.uniform(6.0, 9.5), 1)
            
            # Generate descriptions with Indian context
            descriptions = [
                f"This prestigious scholarship supports outstanding {degree_level} students pursuing {field} in India. Recipients demonstrate exceptional academic achievement and leadership potential in the Indian education system.",
                f"The {title} provides financial assistance to talented Indian students in {field}. This award recognizes academic excellence and commitment to nation-building through education.",
                f"Designed for high-achieving {degree_level} students from India, this scholarship supports those pursuing careers in {field}. Applicants should demonstrate strong academic performance and dedication to their field.",
                f"This competitive scholarship by {provider} is awarded to exceptional Indian students studying {field} at the {degree_level} level. Recipients are selected based on academic merit and potential impact.",
                f"Supporting the next generation of Indian {field} professionals, this scholarship provides significant financial aid to {degree_level} students demonstrating outstanding academic achievement and social commitment.",
                f"The {provider} is proud to offer this scholarship to talented students from India pursuing {field}. This award recognizes both academic excellence and leadership in Indian society.",
                f"This scholarship opportunity is available to Indian {degree_level} students specializing in {field}. Priority given to students from economically weaker sections and rural areas.",
                f"Aimed at fostering excellence in {field} education in India, this scholarship supports promising {degree_level} students who show exceptional academic performance and commitment to national development.",
            ]
            
            description = random.choice(descriptions)
            
            # Generate eligibility with Indian context
            eligibility_templates = [
                f"• Must be enrolled in a {degree_level} program in {field} at a recognized Indian university\n• Minimum CGPA of {gpa_required}/10.0\n• Indian citizen with valid Aadhaar card\n• Demonstrated leadership or community involvement\n• Annual family income below ₹8 lakhs (for need-based)",
                f"• Currently pursuing {degree_level} degree in {field} from UGC/AICTE approved institution\n• CGPA requirement: {gpa_required}/10.0 or higher\n• Indian nationality required\n• Full-time student status\n• Submit SOP and recommendation letters from professors",
                f"• Accepted or enrolled in {degree_level} program in {field}\n• Minimum CGPA: {gpa_required}/10.0\n• Domicile certificate required\n• Leadership experience in college/university preferred\n• Essay submission on 'India's Future in {field}' required",
                f"• {degree_level} student in {field} at Indian institution\n• Academic CGPA of {gpa_required}+/10.0\n• Valid caste certificate (if applicable for reserved categories)\n• Strong recommendation letters from HOD/Principal\n• Income certificate for need-based scholarships\n• No previous scholarship received",
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
                'Sports': 'sports',
                'Research': 'research',
                'Community Service': 'community',
                'Leadership': 'academic'
            }
            type_code = type_map.get(scholarship_type, 'merit')
            category = random.choice(['', 'SC', 'ST', 'OBC', 'MINORITY'])
            max_income = random.choice([800000, 1200000, 2500000, None, None]) if type_code == 'need' else None
            
            # Create scholarship
            try:
                scholarship = Scholarship.objects.create(
                    title=title[:200],  # Ensure title fits in field
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
                    category=category,
                    max_income=max_income,
                    status='active',
                    is_featured=random.choice([True, False]) if i < 15 else False
                )
                scholarships_created += 1
                
                if scholarships_created % 20 == 0:
                    self.stdout.write(self.style.SUCCESS(f'Created {scholarships_created} scholarships...'))
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating scholarship: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully created {scholarships_created} Indian scholarships!'))
        self.stdout.write(self.style.SUCCESS(f'📊 Total scholarships in database: {Scholarship.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'🇮🇳 Indian scholarships: {Scholarship.objects.filter(country="India").count()}'))
        self.stdout.write(self.style.SUCCESS(f'🌍 International scholarships: {Scholarship.objects.exclude(country="India").count()}'))
