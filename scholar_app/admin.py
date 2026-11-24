"""
AI-Scholar Admin Configuration
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import StudentProfile, Scholarship, Application, Document, Notification, RecommendationLog


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'country', 'current_degree', 'gpa', 'profile_complete', 'created_at']
    list_filter = ['current_degree', 'country', 'profile_complete', 'gender']
    search_fields = ['user__username', 'user__email', 'field_of_study', 'institution']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'profile_photo')
        }),
        ('Personal Details', {
            'fields': ('date_of_birth', 'gender', 'phone', 'address', 'city', 'state', 'country', 'zipcode')
        }),
        ('Academic Information', {
            'fields': ('current_degree', 'field_of_study', 'institution', 'gpa', 'graduation_year')
        }),
        ('Additional Information', {
            'fields': ('skills', 'interests', 'achievements', 'extracurricular', 'family_income')
        }),
        ('Metadata', {
            'fields': ('profile_complete', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ['title', 'provider', 'amount', 'scholarship_type', 'country', 'deadline', 'status', 'is_featured', 'applications_count']
    list_filter = ['status', 'scholarship_type', 'degree_level', 'country', 'is_featured', 'provider_type', 'category', 'gender_requirement']
    search_fields = ['title', 'provider', 'description', 'field_of_study', 'state']
    readonly_fields = ['views_count', 'applications_count', 'created_at', 'updated_at']
    date_hierarchy = 'deadline'
    actions = ['mark_as_featured', 'mark_as_active', 'mark_as_expired']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'provider', 'provider_website', 'provider_type')
        }),
        ('Scholarship Details', {
            'fields': ('scholarship_type', 'amount', 'currency', 'number_of_awards')
        }),
        ('Location & Basic Eligibility', {
            'fields': ('country', 'state', 'degree_level', 'field_of_study')
        }),
        ('Academic & Age Criteria', {
            'fields': ('min_gpa', 'max_age')
        }),
        ('Demographic Criteria', {
            'fields': ('gender_requirement', 'category')
        }),
        ('Financial Criteria', {
            'fields': ('max_income',),
            'description': 'Maximum annual family income limit (leave blank if no limit)'
        }),
        ('Dates', {
            'fields': ('application_start', 'deadline', 'notification_date')
        }),
        ('Requirements', {
            'fields': ('required_documents', 'eligibility_criteria', 'application_url')
        }),
        ('Status & Stats', {
            'fields': ('status', 'is_featured', 'views_count', 'applications_count', 'created_by')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
    mark_as_featured.short_description = "Mark selected scholarships as featured"
    
    def mark_as_active(self, request, queryset):
        queryset.update(status='active')
    mark_as_active.short_description = "Mark as active"
    
    def mark_as_expired(self, request, queryset):
        queryset.update(status='expired')
    mark_as_expired.short_description = "Mark as expired"


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['student', 'scholarship', 'status', 'applied_date', 'submitted_date']
    list_filter = ['status', 'applied_date', 'submitted_date']
    search_fields = ['student__username', 'scholarship__title']
    readonly_fields = ['applied_date', 'updated_at']
    date_hierarchy = 'applied_date'
    actions = ['approve_applications', 'reject_applications']
    
    fieldsets = (
        ('Application Info', {
            'fields': ('student', 'scholarship', 'status', 'application_text')
        }),
        ('Dates', {
            'fields': ('applied_date', 'submitted_date', 'reviewed_date', 'decision_date')
        }),
        ('Review', {
            'fields': ('reviewer_notes', 'reviewed_by')
        }),
        ('Metadata', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )
    
    def approve_applications(self, request, queryset):
        queryset.update(status='approved')
    approve_applications.short_description = "Approve selected applications"
    
    def reject_applications(self, request, queryset):
        queryset.update(status='rejected')
    reject_applications.short_description = "Reject selected applications"


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'student', 'document_type', 'is_verified', 'uploaded_at']
    list_filter = ['document_type', 'is_verified', 'uploaded_at']
    search_fields = ['title', 'student__username', 'description']
    readonly_fields = ['uploaded_at', 'file_size']
    date_hierarchy = 'uploaded_at'
    actions = ['verify_documents']
    
    def verify_documents(self, request, queryset):
        from django.utils import timezone
        queryset.update(is_verified=True, verified_by=request.user, verified_at=timezone.now())
    verify_documents.short_description = "Verify selected documents"


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'message', 'user__username']
    readonly_fields = ['created_at', 'read_at']
    date_hierarchy = 'created_at'
    actions = ['mark_as_read']
    
    def mark_as_read(self, request, queryset):
        from django.utils import timezone
        queryset.update(is_read=True, read_at=timezone.now())
    mark_as_read.short_description = "Mark as read"


@admin.register(RecommendationLog)
class RecommendationLogAdmin(admin.ModelAdmin):
    list_display = ['student', 'scholarship', 'match_score', 'was_viewed', 'was_applied', 'recommended_at']
    list_filter = ['was_viewed', 'was_applied', 'recommended_at']
    search_fields = ['student__username', 'scholarship__title']
    readonly_fields = ['recommended_at']
    date_hierarchy = 'recommended_at'


# Customize admin site
admin.site.site_header = "AI-Scholar Administration"
admin.site.site_title = "AI-Scholar Admin"
admin.site.index_title = "Welcome to AI-Scholar Admin Portal"
