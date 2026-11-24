"""
AI-Scholar Models
Database models for the scholarship recommendation system
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class StudentProfile(models.Model):
    """Student profile with academic and personal information"""
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say'),
    ]
    
    DEGREE_CHOICES = [
        ('HS', 'High School'),
        ('UG', 'Undergraduate'),
        ('PG', 'Postgraduate'),
        ('PHD', 'PhD'),
    ]
    
    CATEGORY_CHOICES = [
        ('GEN', 'General'),
        ('SC', 'Scheduled Caste'),
        ('ST', 'Scheduled Tribe'),
        ('OBC', 'Other Backward Class'),
        ('EWS', 'Economically Weaker Section'),
        ('MINORITY', 'Minority'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Personal Information
    full_name = models.CharField(max_length=200, blank=True, help_text="Full Name")
    age = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(5), MaxValueValidator(100)])
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='N')
    phone = models.CharField(max_length=20, blank=True, unique=True, null=True)
    phone_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    
    # Address Information
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='India')
    zipcode = models.CharField(max_length=20, blank=True)
    
    # Category and Financial
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='GEN')
    family_income = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Annual family income in INR"
    )
    
    # Academic Information (Education Level)
    education_level = models.CharField(max_length=3, choices=DEGREE_CHOICES, default='UG', help_text="Current Education Level")
    current_degree = models.CharField(max_length=3, choices=DEGREE_CHOICES, default='UG')
    field_of_study = models.CharField(max_length=200, blank=True, help_text="Course/Stream")
    course_stream = models.CharField(max_length=200, blank=True, help_text="Course or Stream (e.g., B.Tech, B.A., M.Sc.)")
    institution = models.CharField(max_length=200, blank=True)
    
    # Marks/CGPA
    marks_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Marks in percentage (0-100)"
    )
    gpa = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        validators=[MinValueValidator(1.0), MaxValueValidator(10.0)],
        null=True,
        blank=True,
        help_text="CGPA on 10.0 scale (Indian system, 1.0-10.0)"
    )
    graduation_year = models.IntegerField(null=True, blank=True)
    
    # Additional Information
    skills = models.TextField(help_text="Comma-separated skills", blank=True)
    interests = models.TextField(help_text="Comma-separated interests (e.g., Science, Arts, Sports)", blank=True)
    achievements = models.TextField(blank=True)
    extracurricular = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True, help_text="Current Location")
    
    # Profile completion
    profile_complete = models.BooleanField(default=False)
    profile_photo = models.ImageField(upload_to='profiles/', null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}'s Profile"
    
    def calculate_profile_completion(self):
        """Calculate profile completion percentage"""
        fields = [
            self.full_name, self.age, self.gender, self.phone, self.country,
            self.category, self.family_income, self.education_level, 
            self.field_of_study, self.institution, self.gpa, 
            self.skills, self.interests, self.location
        ]
        completed = sum(1 for field in fields if field)
        return int((completed / len(fields)) * 100)
    
    def get_age(self):
        """Calculate age from date of birth"""
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return self.age


class OTPVerification(models.Model):
    """OTP verification for phone and email"""
    
    VERIFICATION_TYPE = [
        ('email', 'Email'),
        ('phone', 'Phone'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_verifications', null=True, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    otp_code = models.CharField(max_length=6)
    verification_type = models.CharField(max_length=10, choices=VERIFICATION_TYPE)
    
    is_verified = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    verified_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'OTP Verification'
        verbose_name_plural = 'OTP Verifications'
    
    def __str__(self):
        return f"OTP for {self.email or self.phone} - {self.verification_type}"
    
    def is_valid(self):
        """Check if OTP is still valid"""
        if self.is_expired or self.is_verified:
            return False
        return timezone.now() < self.expires_at
    
    def verify(self, code):
        """Verify the OTP code"""
        if self.is_valid() and self.otp_code == code:
            self.is_verified = True
            self.verified_at = timezone.now()
            self.save()
            return True
        return False


class Scholarship(models.Model):
    """Scholarship information and eligibility criteria"""
    
    TYPE_CHOICES = [
        ('merit', 'Merit-Based'),
        ('need', 'Need-Based'),
        ('sports', 'Sports'),
        ('academic', 'Academic Excellence'),
        ('minority', 'Minority'),
        ('women', 'Women in STEM'),
        ('research', 'Research'),
        ('community', 'Community Service'),
    ]
    
    DEGREE_CHOICES = [
        ('HS', 'High School'),
        ('UG', 'Undergraduate'),
        ('PG', 'Postgraduate'),
        ('PHD', 'PhD'),
        ('ALL', 'All Levels'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('expired', 'Expired'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=300)
    description = models.TextField()
    provider = models.CharField(max_length=200, help_text="Organization providing the scholarship")
    provider_website = models.URLField(blank=True)
    
    # Scholarship Details
    scholarship_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='merit')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    number_of_awards = models.IntegerField(default=1)
    
    # Eligibility
    country = models.CharField(max_length=100, default='USA')
    state = models.CharField(max_length=100, blank=True, help_text="State/Province (especially for India)")
    degree_level = models.CharField(max_length=3, choices=DEGREE_CHOICES, default='UG')
    field_of_study = models.CharField(max_length=200, blank=True, help_text="Comma-separated fields")
    min_gpa = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        validators=[MinValueValidator(1.0), MaxValueValidator(10.0)],
        null=True,
        blank=True,
        help_text="Minimum CGPA on 10.0 scale (Indian system, 1.0-10.0)"
    )
    max_age = models.IntegerField(null=True, blank=True)
    gender_requirement = models.CharField(max_length=1, blank=True, choices=[
        ('M', 'Male Only'),
        ('F', 'Female Only'),
        ('', 'All Genders'),
    ])
    
    # Additional Eligibility Criteria
    category = models.CharField(max_length=20, blank=True, choices=[
        ('', 'All Categories'),
        ('SC', 'Scheduled Caste'),
        ('ST', 'Scheduled Tribe'),
        ('OBC', 'Other Backward Class'),
        ('MINORITY', 'Minority'),
    ], help_text="Caste/Category requirement")
    max_income = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Maximum annual family income (in INR/USD)"
    )
    provider_type = models.CharField(max_length=20, blank=True, choices=[
        ('', 'Not Specified'),
        ('government', 'Government'),
        ('private', 'Private/NGO'),
    ], help_text="Type of organization providing the scholarship")
    
    # Dates
    application_start = models.DateField(null=True, blank=True)
    deadline = models.DateField()
    notification_date = models.DateField(null=True, blank=True)
    
    # Requirements
    required_documents = models.TextField(blank=True, help_text="List of required documents")
    eligibility_criteria = models.TextField()
    application_url = models.URLField(blank=True)
    
    # Status
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    is_featured = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)
    applications_count = models.IntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='scholarships_created')
    
    class Meta:
        ordering = ['-created_at', 'deadline']
        verbose_name = 'Scholarship'
        verbose_name_plural = 'Scholarships'
        indexes = [
            models.Index(fields=['status', 'deadline']),
            models.Index(fields=['country', 'degree_level']),
        ]
    
    def __str__(self):
        return self.title
    
    def is_expired(self):
        """Check if scholarship deadline has passed"""
        return self.deadline < timezone.now().date()
    
    def days_until_deadline(self):
        """Calculate days until deadline"""
        delta = self.deadline - timezone.now().date()
        return delta.days if delta.days > 0 else 0


class Application(models.Model):
    """Student scholarship applications"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE, related_name='applications')
    
    # Application Details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    application_text = models.TextField(blank=True, help_text="Personal statement or essay")
    
    # Dates
    applied_date = models.DateTimeField(auto_now_add=True)
    submitted_date = models.DateTimeField(null=True, blank=True)
    reviewed_date = models.DateTimeField(null=True, blank=True)
    decision_date = models.DateTimeField(null=True, blank=True)
    
    # Review
    reviewer_notes = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='reviewed_applications'
    )
    
    # Metadata
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-applied_date']
        unique_together = ['student', 'scholarship']
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['scholarship', 'status']),
        ]
    
    def __str__(self):
        return f"{self.student.username} - {self.scholarship.title}"


class Document(models.Model):
    """Documents uploaded by students"""
    
    DOC_TYPE_CHOICES = [
        ('resume', 'Resume/CV'),
        ('transcript', 'Academic Transcript'),
        ('certificate', 'Certificate'),
        ('id_proof', 'ID Proof'),
        ('income', 'Income Certificate'),
        ('recommendation', 'Recommendation Letter'),
        ('essay', 'Essay'),
        ('other', 'Other'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    application = models.ForeignKey(
        Application, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='documents'
    )
    
    document_type = models.CharField(max_length=20, choices=DOC_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/%Y/%m/')
    description = models.TextField(blank=True)
    
    # Verification
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='verified_documents'
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.IntegerField(help_text="File size in bytes", default=0)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
    
    def __str__(self):
        return f"{self.title} - {self.student.username}"


class Notification(models.Model):
    """System notifications for users"""
    
    TYPE_CHOICES = [
        ('deadline', 'Deadline Reminder'),
        ('status', 'Application Status Update'),
        ('new_scholarship', 'New Scholarship'),
        ('document', 'Document Request'),
        ('system', 'System Notification'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='system')
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    # Related objects
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE, null=True, blank=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, null=True, blank=True)
    
    # Status
    is_read = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        indexes = [
            models.Index(fields=['user', 'is_read']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()


class RecommendationLog(models.Model):
    """Log of AI recommendations for analysis"""
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendation_logs')
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE)
    
    match_score = models.DecimalField(max_digits=5, decimal_places=2, help_text="Match percentage")
    recommendation_reason = models.TextField(blank=True)
    
    # User interaction
    was_viewed = models.BooleanField(default=False)
    was_applied = models.BooleanField(default=False)
    
    # Metadata
    recommended_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-recommended_at']
        unique_together = ['student', 'scholarship', 'recommended_at']
        verbose_name = 'Recommendation Log'
        verbose_name_plural = 'Recommendation Logs'
    
    def __str__(self):
        return f"{self.student.username} - {self.scholarship.title} ({self.match_score}%)"
