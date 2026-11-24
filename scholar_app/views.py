"""
AI-Scholar Views
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

from .models import StudentProfile, Scholarship, Application, Document, Notification, RecommendationLog, OTPVerification



def home(request):
    """Homepage view"""

    featured_scholarships = Scholarship.objects.filter(
        status='active',
        is_featured=True,
        deadline__gte=timezone.localdate()
    ).order_by('-created_at')[:6]

    # If no featured scholarships exist, show latest active scholarships
    if not featured_scholarships.exists():
        featured_scholarships = Scholarship.objects.filter(
            status='active',
            deadline__gte=timezone.localdate()
        ).order_by('-created_at')[:6]

    context = {
        'today': timezone.localdate(),
        'featured_scholarships': featured_scholarships,
    }

    return render(request, 'index.html', context)


def scholarships_list(request):
    """Browse all scholarships with comprehensive filters"""
    scholarships = Scholarship.objects.filter(status='active', deadline__gte=timezone.localdate())
    
    # Apply filters
    search = request.GET.get('search')
    if search:
        scholarships = scholarships.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(provider__icontains=search) |
            Q(field_of_study__icontains=search) |
            Q(country__icontains=search) |
            Q(eligibility_criteria__icontains=search)
        )
    
    # Type of Scholarship
    scholarship_type = request.GET.get('type')
    if scholarship_type:
        scholarships = scholarships.filter(scholarship_type=scholarship_type)
    
    # Course/Stream (Field of Study)
    course = request.GET.get('course')
    if course:
        scholarships = scholarships.filter(field_of_study__icontains=course)
    
    # Location/Country/State
    country = request.GET.get('country')
    if country:
        scholarships = scholarships.filter(country__icontains=country)
    
    state = request.GET.get('state')
    if state:
        scholarships = scholarships.filter(
            Q(country__icontains=state) |
            Q(eligibility_criteria__icontains=state)
        )
    
    # Degree Level
    degree_level = request.GET.get('degree_level')
    if degree_level:
        scholarships = scholarships.filter(
            Q(degree_level=degree_level) | Q(degree_level='ALL')
        )
    
    # Gender
    gender = request.GET.get('gender')
    if gender:
        scholarships = scholarships.filter(
            Q(gender_requirement=gender) | 
            Q(gender_requirement__isnull=True) | 
            Q(gender_requirement='')
        )
    
    # Category (SC/ST/OBC/Minority)
    category = request.GET.get('category')
    if category:
        scholarships = scholarships.filter(
            Q(category=category) |
            Q(category='') |
            Q(eligibility_criteria__icontains=category)
        )
    
    # Financial Criteria
    min_amount = request.GET.get('min_amount')
    if min_amount:
        scholarships = scholarships.filter(amount__gte=float(min_amount))
    
    max_amount = request.GET.get('max_amount')
    if max_amount:
        scholarships = scholarships.filter(amount__lte=float(max_amount))
    
    max_income = request.GET.get('max_income')
    if max_income:
        try:
            income = float(max_income)
            scholarships = scholarships.filter(
                Q(max_income__isnull=True) |
                Q(max_income__gte=income)
            )
        except (TypeError, ValueError):
            pass
    
    # Academic Criteria (GPA/Marks)
    min_gpa = request.GET.get('min_gpa')
    if min_gpa:
        scholarships = scholarships.filter(
            Q(min_gpa__lte=float(min_gpa)) | Q(min_gpa__isnull=True)
        )
    
    # Age Criteria
    age = request.GET.get('age')
    if age:
        scholarships = scholarships.filter(
            Q(max_age__gte=int(age)) | Q(max_age__isnull=True)
        )
    
    # Provider Type (Government/Private)
    provider_type = request.GET.get('provider_type')
    if provider_type:
        if provider_type == 'government':
            scholarships = scholarships.filter(
                Q(provider__icontains='government') |
                Q(provider__icontains='ministry') |
                Q(provider__icontains='ugc') |
                Q(provider__icontains='state')
            )
        elif provider_type == 'private':
            scholarships = scholarships.exclude(
                Q(provider__icontains='government') |
                Q(provider__icontains='ministry') |
                Q(provider__icontains='ugc')
            )
    
    # Sort
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by == 'amount_high':
        scholarships = scholarships.order_by('-amount')
    elif sort_by == 'amount_low':
        scholarships = scholarships.order_by('amount')
    elif sort_by == 'deadline':
        scholarships = scholarships.order_by('deadline')
    elif sort_by == 'popular':
        scholarships = scholarships.order_by('-views_count')
    else:
        scholarships = scholarships.order_by('-created_at')
    
    context = {
        'today': timezone.localdate(),
        'scholarships': scholarships,
        'total_count': scholarships.count(),
        # Preserve current filter values
        'current_search': search or '',
        'current_type': scholarship_type or '',
        'current_course': course or '',
        'current_country': country or '',
        'current_state': state or '',
        'current_degree': degree_level or '',
        'current_gender': gender or '',
        'current_category': category or '',
        'current_provider_type': provider_type or '',
        'current_sort': sort_by,
    }
    return render(request, 'scholarships.html', context)


def scholarship_detail(request, scholarship_id):
    """Detailed view of a scholarship"""
    scholarship = get_object_or_404(Scholarship, id=scholarship_id)
    scholarship.views_count += 1
    scholarship.save()
    
    context = {
        'today': timezone.localdate(),
        'scholarship': scholarship,
    }
    return render(request, 'scholarship_detail.html', context)


@login_required
def dashboard(request):
    """Student dashboard"""
    try:
        profile = request.user.profile
    except StudentProfile.DoesNotExist:
        profile = StudentProfile.objects.create(user=request.user)
    
    # Get user's applications
    applications = Application.objects.filter(student=request.user)
    
    # Get personalized recommendations from the AI engine
    from ai_engine.recommendation_model import get_recommender

    available_scholarships = Scholarship.objects.filter(
        status='active',
        deadline__gte=timezone.localdate()
    )
    recommendation_results = get_recommender().get_recommendations(
        profile,
        available_scholarships,
        top_n=4
    )
    recommendations = []
    for result in recommendation_results:
        scholarship = result['scholarship']
        scholarship.match_score = result['match_score']
        recommendations.append(scholarship)
    
    # Calculate stats
    applied_count = applications.count()
    pending_count = applications.filter(status='submitted').count()
    approved_count = applications.filter(status='approved').count()
    
    # Upcoming deadlines
    upcoming_deadlines = []
    for app in applications.filter(status='submitted'):
        if not app.scholarship.deadline:
            continue
        days_left = (app.scholarship.deadline - timezone.localdate()).days
        if days_left > 0 and days_left <= 30:
            upcoming_deadlines.append({
                'scholarship': app.scholarship,
                'days_left': days_left
            })
    
    context = {
        'today': timezone.localdate(),
        'profile': profile,
        'applications': applications[:10],
        'recommendations': recommendations,
        'recommended_count': len(recommendations),
        'applied_count': applied_count,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'upcoming_deadlines': upcoming_deadlines,
    }
    return render(request, 'dashboard.html', context)


@login_required
def profile_view(request):
    """User profile view and edit"""
    try:
        profile = request.user.profile
    except StudentProfile.DoesNotExist:
        profile = StudentProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        # Update personal information
        profile.full_name = request.POST.get('full_name', '')
        age = request.POST.get('age')
        if age:
            profile.age = int(age)
        profile.gender = request.POST.get('gender', 'N')
        profile.phone = request.POST.get('phone', '')
        profile.category = request.POST.get('category', 'GEN')
        
        family_income = request.POST.get('family_income')
        if family_income:
            profile.family_income = float(family_income)
        
        # Update address information
        profile.city = request.POST.get('city', '')
        profile.state = request.POST.get('state', '')
        profile.country = request.POST.get('country', 'India')
        profile.location = request.POST.get('location', '')
        profile.zipcode = request.POST.get('zipcode', '')
        
        # Update academic information
        profile.education_level = request.POST.get('education_level', '')
        profile.current_degree = request.POST.get('education_level', '')
        profile.course_stream = request.POST.get('course_stream', '')
        profile.field_of_study = request.POST.get('field_of_study', '')
        profile.institution = request.POST.get('institution', '')
        
        gpa = request.POST.get('gpa')
        if gpa:
            profile.gpa = float(gpa)
        
        marks_percentage = request.POST.get('marks_percentage')
        if marks_percentage:
            profile.marks_percentage = float(marks_percentage)
        
        graduation_year = request.POST.get('graduation_year')
        if graduation_year:
            profile.graduation_year = int(graduation_year)
        
        # Update additional information
        profile.skills = request.POST.get('skills', '')
        profile.interests = request.POST.get('interests', '')
        profile.achievements = request.POST.get('achievements', '')
        profile.extracurricular = request.POST.get('extracurricular', '')
        
        # Calculate and update profile completion
        completion = profile.calculate_profile_completion()
        profile.profile_complete = completion >= 80
        
        profile.save()
        
        messages.success(request, f'Profile updated successfully! Profile completion: {completion}%')
        return redirect('profile')
    
    context = {
        'profile': profile,
    }
    return render(request, 'profile.html', context)


@login_required
def apply_scholarship(request, scholarship_id):
    """Apply to a scholarship"""
    scholarship = get_object_or_404(Scholarship, id=scholarship_id)
    
    # Check if already applied
    existing_application = Application.objects.filter(
        student=request.user,
        scholarship=scholarship
    ).first()
    
    if existing_application:
        messages.warning(request, 'You have already applied to this scholarship.')
        return redirect('scholarship_detail', scholarship_id=scholarship_id)
    
    if request.method == 'POST':
        application_text = request.POST.get('application_text', '')
        
        application = Application.objects.create(
            student=request.user,
            scholarship=scholarship,
            status='submitted',
            application_text=application_text,
            submitted_date=timezone.now()
        )
        
        # Update scholarship application count
        scholarship.applications_count += 1
        scholarship.save()
        
        messages.success(request, 'Application submitted successfully!')
        return redirect('dashboard')
    
    context = {
        'scholarship': scholarship,
    }
    return render(request, 'apply.html', context)


@login_required
def chatbot_view(request):
    """Chatbot interface"""
    return render(request, 'chatbot.html')


@require_POST
def chatbot_api(request):
    """Enhanced AI Chatbot API endpoint"""
    try:
        data = json.loads(request.body)
        message = data.get('message', '')
        
        if not message:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        # Use enhanced chatbot engine
        from .chatbot_engine import get_chatbot_response
        
        # Allow both authenticated and anonymous users
        user = request.user if request.user.is_authenticated else None
        response = get_chatbot_response(message, user)
        
        return JsonResponse({'response': response})
    except Exception as e:
        import traceback
        print(f"Chatbot error: {str(e)}")
        print(traceback.format_exc())
        return JsonResponse({
            'response': "Sorry, I encountered an error. Please try again! 😊"
        })


def register_view(request):
    """User registration with profile setup"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Create user
            user = form.save(commit=False)
            email = request.POST.get('email')
            if email:
                user.email = email
            user.save()
            
            # Create profile with additional data from registration
            profile = StudentProfile.objects.create(user=user)
            
            # Update profile with registration data if provided
            phone = request.POST.get('phone')
            if phone:
                profile.phone = phone
            
            full_name = request.POST.get('full_name')
            if full_name:
                profile.full_name = full_name
            
            age = request.POST.get('age')
            if age:
                try:
                    profile.age = int(age)
                except:
                    pass
            
            gender = request.POST.get('gender')
            if gender:
                profile.gender = gender
            
            category = request.POST.get('category')
            if category:
                profile.category = category
            
            education_level = request.POST.get('education_level')
            if education_level:
                profile.education_level = education_level
                profile.current_degree = education_level
            
            course_stream = request.POST.get('course_stream')
            if course_stream:
                profile.course_stream = course_stream
            
            gpa = request.POST.get('gpa')
            if gpa:
                try:
                    profile.gpa = float(gpa)
                except:
                    pass
            
            marks_percentage = request.POST.get('marks_percentage')
            if marks_percentage:
                try:
                    profile.marks_percentage = float(marks_percentage)
                except:
                    pass
            
            family_income = request.POST.get('family_income')
            if family_income:
                try:
                    profile.family_income = float(family_income)
                except:
                    pass
            
            location = request.POST.get('location')
            if location:
                profile.location = location
            
            interests = request.POST.get('interests')
            if interests:
                profile.interests = interests
            
            profile.save()
            
            # Log the user in
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to AI-Scholar!')
            return redirect('dashboard')
        else:
            # Form has errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


def admin_register_view(request):
    """Admin registration - create new admin account"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'admin_register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'admin_register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'admin_register.html')
        
        try:
            # Create admin user with staff privileges
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.is_staff = True  # Make user an admin
            user.save()
            
            messages.success(request, 'Admin account created successfully! Please login.')
            return redirect('admin_login')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
    
    return render(request, 'admin_register.html')


def admin_login_view(request):
    """Admin login - separate from regular user login"""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_staff:  # Check if user is admin/staff
                login(request, user)
                messages.success(request, f'Welcome Admin {username}!')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'You do not have admin privileges.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'admin_login.html')


@login_required
def logout_view(request):
    """User logout"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


@require_POST
def send_otp(request):
    """Send OTP for verification"""
    try:
        data = json.loads(request.body)
        identifier = data.get('identifier')  # email or phone
        verification_type = data.get('type', 'email')  # email or phone
        
        if not identifier:
            return JsonResponse({'error': 'Identifier is required'}, status=400)
        
        # Generate 6-digit OTP
        import random
        otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        # Create OTP verification record
        from datetime import timedelta
        expires_at = timezone.now() + timedelta(minutes=5)
        
        otp = OTPVerification.objects.create(
            email=identifier if verification_type == 'email' else '',
            phone=identifier if verification_type == 'phone' else '',
            otp_code=otp_code,
            verification_type=verification_type,
            expires_at=expires_at,
            user=request.user if request.user.is_authenticated else None
        )
        
        # In production, send actual OTP via email/SMS
        # For now, log it (in production, remove this!)
        print(f"OTP for {identifier}: {otp_code}")
        
        return JsonResponse({
            'success': True,
            'message': f'OTP sent to {identifier}',
            'otp_id': otp.id,
            # In production, NEVER return the actual OTP!
            'debug_otp': otp_code  # Remove in production!
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_POST
def verify_otp(request):
    """Verify OTP code"""
    try:
        data = json.loads(request.body)
        otp_id = data.get('otp_id')
        otp_code = data.get('otp_code')
        
        if not otp_id or not otp_code:
            return JsonResponse({'error': 'OTP ID and code are required'}, status=400)
        
        try:
            otp = OTPVerification.objects.get(id=otp_id)
        except OTPVerification.DoesNotExist:
            return JsonResponse({'error': 'Invalid OTP'}, status=404)
        
        if otp.verify(otp_code):
            # Update user's verification status
            if request.user.is_authenticated:
                profile = request.user.profile
                if otp.verification_type == 'email':
                    profile.email_verified = True
                elif otp.verification_type == 'phone':
                    profile.phone_verified = True
                profile.save()
            
            return JsonResponse({
                'success': True,
                'message': 'OTP verified successfully'
            })
        else:
            return JsonResponse({
                'error': 'Invalid or expired OTP'
            }, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def admin_dashboard(request):
    """Admin dashboard - separate from Django admin"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    # Admin statistics
    total_students = StudentProfile.objects.count()
    total_scholarships = Scholarship.objects.count()
    active_scholarships = Scholarship.objects.filter(status='active').count()
    total_applications = Application.objects.count()
    pending_applications = Application.objects.filter(status='submitted').count()
    
    # Recent data for tables
    recent_scholarships = Scholarship.objects.all().order_by('-created_at')[:10]
    recent_applications = Application.objects.all().order_by('-applied_date')[:10]
    recent_users = StudentProfile.objects.all().order_by('-created_at')[:10]
    
    context = {
        'total_students': total_students,
        'total_scholarships': total_scholarships,
        'active_scholarships': active_scholarships,
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'recent_scholarships': recent_scholarships,
        'recent_applications': recent_applications,
        'recent_users': recent_users,
    }
    return render(request, 'admin_dashboard.html', context)


@login_required
def add_scholarship(request):
    """Add new scholarship - admin only"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    if request.method == 'POST':
        try:
            # Create scholarship from form data
            scholarship = Scholarship.objects.create(
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                provider=request.POST.get('provider'),
                provider_website=request.POST.get('provider_website', ''),
                provider_type=request.POST.get('provider_type', ''),
                scholarship_type=request.POST.get('scholarship_type'),
                amount=request.POST.get('amount'),
                currency=request.POST.get('currency', 'USD'),
                number_of_awards=request.POST.get('number_of_awards', 1),
                country=request.POST.get('country'),
                state=request.POST.get('state', ''),
                degree_level=request.POST.get('degree_level'),
                field_of_study=request.POST.get('field_of_study', ''),
                min_gpa=request.POST.get('min_gpa') if request.POST.get('min_gpa') else None,
                max_age=request.POST.get('max_age') if request.POST.get('max_age') else None,
                gender_requirement=request.POST.get('gender_requirement', ''),
                category=request.POST.get('category', ''),
                max_income=request.POST.get('max_income') if request.POST.get('max_income') else None,
                deadline=request.POST.get('deadline'),
                application_start=request.POST.get('application_start') if request.POST.get('application_start') else None,
                notification_date=request.POST.get('notification_date') if request.POST.get('notification_date') else None,
                required_documents=request.POST.get('required_documents', ''),
                eligibility_criteria=request.POST.get('eligibility_criteria'),
                application_url=request.POST.get('application_url', ''),
                status=request.POST.get('status', 'active'),
                is_featured=request.POST.get('is_featured') == 'on',
                created_by=request.user
            )
            
            messages.success(request, f'Scholarship "{scholarship.title}" has been added successfully!')
            return redirect('admin_dashboard')
            
        except Exception as e:
            messages.error(request, f'Error adding scholarship: {str(e)}')
    
    return render(request, 'add_scholarship.html')


@login_required
def manage_scholarships(request):
    """List and manage all scholarships - admin only"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    scholarships = Scholarship.objects.all().order_by('-created_at')
    
    context = {
        'scholarships': scholarships,
    }
    return render(request, 'manage_scholarships.html', context)


@login_required
def edit_scholarship(request, scholarship_id):
    """Edit scholarship - admin only"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    scholarship = get_object_or_404(Scholarship, id=scholarship_id)
    
    if request.method == 'POST':
        try:
            scholarship.title = request.POST.get('title')
            scholarship.description = request.POST.get('description')
            scholarship.provider = request.POST.get('provider')
            scholarship.provider_website = request.POST.get('provider_website', '')
            scholarship.provider_type = request.POST.get('provider_type', '')
            scholarship.scholarship_type = request.POST.get('scholarship_type')
            scholarship.amount = request.POST.get('amount')
            scholarship.currency = request.POST.get('currency', 'USD')
            scholarship.number_of_awards = request.POST.get('number_of_awards', 1)
            scholarship.country = request.POST.get('country')
            scholarship.state = request.POST.get('state', '')
            scholarship.degree_level = request.POST.get('degree_level')
            scholarship.field_of_study = request.POST.get('field_of_study', '')
            scholarship.min_gpa = request.POST.get('min_gpa') if request.POST.get('min_gpa') else None
            scholarship.max_age = request.POST.get('max_age') if request.POST.get('max_age') else None
            scholarship.gender_requirement = request.POST.get('gender_requirement', '')
            scholarship.category = request.POST.get('category', '')
            scholarship.max_income = request.POST.get('max_income') if request.POST.get('max_income') else None
            scholarship.deadline = request.POST.get('deadline')
            scholarship.application_start = request.POST.get('application_start') if request.POST.get('application_start') else None
            scholarship.notification_date = request.POST.get('notification_date') if request.POST.get('notification_date') else None
            scholarship.required_documents = request.POST.get('required_documents', '')
            scholarship.eligibility_criteria = request.POST.get('eligibility_criteria')
            scholarship.application_url = request.POST.get('application_url', '')
            scholarship.status = request.POST.get('status', 'active')
            scholarship.is_featured = request.POST.get('is_featured') == 'on'
            
            scholarship.save()
            
            messages.success(request, f'Scholarship "{scholarship.title}" has been updated successfully!')
            return redirect('manage_scholarships')
            
        except Exception as e:
            messages.error(request, f'Error updating scholarship: {str(e)}')
    
    context = {
        'scholarship': scholarship,
    }
    return render(request, 'edit_scholarship.html', context)


@login_required
def delete_scholarship(request, scholarship_id):
    """Delete scholarship - admin only"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    scholarship = get_object_or_404(Scholarship, id=scholarship_id)
    
    if request.method == 'POST':
        title = scholarship.title
        scholarship.delete()
        messages.success(request, f'Scholarship "{title}" has been deleted successfully!')
        return redirect('manage_scholarships')
    
    context = {
        'scholarship': scholarship,
    }
    return render(request, 'delete_scholarship.html', context)


@login_required
def manage_applications(request):
    """View and manage all applications - admin only"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    applications = Application.objects.all().order_by('-applied_date')
    
    context = {
        'applications': applications,
    }
    return render(request, 'manage_applications.html', context)


@login_required
def review_application(request, application_id):
    """Review and update application status - admin only"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    application = get_object_or_404(Application, id=application_id)
    
    if request.method == 'POST':
        application.status = request.POST.get('status')
        application.reviewer_notes = request.POST.get('reviewer_notes', '')
        application.reviewed_by = request.user
        application.reviewed_date = timezone.now()
        
        if application.status in ['approved', 'rejected']:
            application.decision_date = timezone.now()
        
        application.save()
        
        messages.success(request, f'Application status updated to {application.get_status_display()}')
        return redirect('manage_applications')
    
    context = {
        'application': application,
    }
    return render(request, 'review_application.html', context)


@login_required
def manage_users(request):
    """View and manage all users - admin only"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    users = StudentProfile.objects.all().order_by('-created_at')
    
    context = {
        'users': users,
    }
    return render(request, 'manage_users.html', context)


@login_required
def application_detail(request, application_id):
    """View application details"""
    application = get_object_or_404(Application, id=application_id, student=request.user)
    
    context = {
        'application': application,
    }
    return render(request, 'application_detail.html', context)
