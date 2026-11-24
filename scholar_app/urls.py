"""
AI-Scholar App URLs
"""

from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('scholarships/', views.scholarships_list, name='scholarships'),
    path('scholarship/<int:scholarship_id>/', views.scholarship_detail, name='scholarship_detail'),
    
    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('login/admin/', views.admin_login_view, name='admin_login'),
    path('register/admin/', views.admin_register_view, name='admin_register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Student pages
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('apply/<int:scholarship_id>/', views.apply_scholarship, name='apply'),
    path('application/<int:application_id>/', views.application_detail, name='application_detail'),
    
    # Chatbot
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'),
    
    # OTP Verification
    path('api/send-otp/', views.send_otp, name='send_otp'),
    path('api/verify-otp/', views.verify_otp, name='verify_otp'),
    
    # Custom Admin Dashboard (separate from Django admin at /admin/)
    path('dashboard-admin/', views.admin_dashboard, name='admin_dashboard'),
    path('scholarship/add/', views.add_scholarship, name='add_scholarship'),
    path('scholarships/manage/', views.manage_scholarships, name='manage_scholarships'),
    path('scholarship/edit/<int:scholarship_id>/', views.edit_scholarship, name='edit_scholarship'),
    path('scholarship/delete/<int:scholarship_id>/', views.delete_scholarship, name='delete_scholarship'),
    path('applications/manage/', views.manage_applications, name='manage_applications'),
    path('application/review/<int:application_id>/', views.review_application, name='review_application'),
    path('users/manage/', views.manage_users, name='manage_users'),
]
