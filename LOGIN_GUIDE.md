# 🔐 AI-Scholar Login Guide

## 📌 **Quick Navigation**
- [User Login](#-user-login)
- [Admin Login](#-admin-login)
- [Features Comparison](#-features-comparison)
- [First Time Setup](#-first-time-setup)

---

## 👤 **USER LOGIN**

### **How to Login as a Regular User/Student**

#### **🌐 Access URL:**
```
http://127.0.0.1:8000/login/
```

#### **📋 Login Methods:**

### **Method 1: Password Login** (Recommended for Quick Access)

1. **Navigate to Login Page**
   - Open your browser
   - Go to: `http://127.0.0.1:8000/login/`

2. **Enter Credentials**
   - **Username or Email:** Your registered username or email address
   - **Password:** Your account password (minimum 8 characters)
   
3. **Optional Settings**
   - ☑️ Check "Remember Me" (keeps you logged in for 30 days)
   
4. **Click "Login"** button
   
5. **Success!** You'll be redirected to your Dashboard

**Forgot Password?**
- Click the "Forgot Password?" link below the login form
- Follow the password reset instructions

---

### **Method 2: OTP Login** (Passwordless Login)

1. **Navigate to Login Page**
   - Go to: `http://127.0.0.1:8000/login/`

2. **Switch to OTP Tab**
   - Click on the "**OTP Login**" tab at the top

3. **Enter Contact Information**
   - Type your registered **Email address** OR **Phone number**

4. **Request OTP**
   - Click "**Send OTP**" button
   - A 6-digit OTP will be sent to your email/phone

5. **Enter OTP**
   - Type the 6-digit code you received
   - OTP is valid for **5 minutes**
   - Auto-submits when you enter all 6 digits

6. **Resend Option**
   - If you didn't receive the OTP, click "**Resend OTP**"
   - Wait for the countdown timer to finish before resending

7. **Success!** You'll be redirected to your Dashboard

---

### **🎯 Features Available for Regular Users**

After logging in, users can access:

#### **1. Dashboard** 📊
- URL: `http://127.0.0.1:8000/dashboard/`
- **Features:**
  - View personalized scholarship recommendations
  - See your application status
  - Quick access to profile
  - View applied scholarships
  - Track application progress
  - Scholarship statistics

#### **2. Browse Scholarships** 🔍
- URL: `http://127.0.0.1:8000/scholarships/`
- **Features:**
  - Search scholarships by name, category, or keywords
  - Filter by eligibility criteria
  - View detailed scholarship information
  - Check application deadlines
  - See eligibility requirements

#### **3. Scholarship Details & Apply** 📝
- URL: `http://127.0.0.1:8000/scholarship/<id>/`
- **Features:**
  - View complete scholarship details
  - Check eligibility criteria
  - Application process information
  - Award amount and benefits
  - Important dates and deadlines
  - Apply button (if eligible)

#### **4. Profile Management** 👤
- URL: `http://127.0.0.1:8000/profile/`
- **Features:**
  - **View Profile:** See all your information at a glance
  - **Edit Profile:** Update any field
  - **Profile Sections:**
    - Personal Information (Name, Age, Gender, Category, Income)
    - Address Information (City, State, Country)
    - Academic Information (Education, CGPA, Marks, Course)
    - Additional Information (Skills, Interests, Achievements)
  - **Profile Completion:** Track profile completion percentage
  - **Quick Fill:** Demo data for testing
  
#### **5. Application Tracking** 📋
- URL: `http://127.0.0.1:8000/application/<id>/`
- **Features:**
  - View submitted applications
  - Check application status (Pending/Approved/Rejected)
  - Download application copy
  - Track review progress

#### **6. AI Chatbot** 🤖
- URL: `http://127.0.0.1:8000/chatbot/`
- **Features:**
  - Ask questions about scholarships
  - Get personalized recommendations
  - Guidance on application process
  - Answer eligibility queries
  - 24/7 assistance

---

## 👨‍💼 **ADMIN LOGIN**

### **How to Login as an Administrator**

#### **🌐 Access URL:**
```
    http://127.0.0.1:8000/login/admin/
```

#### **📋 Login Credentials:**

1. **Navigate to Admin Login Page**
   - Open your browser
   - Go to: `http://127.0.0.1:8000/login/admin/`

2. **Enter Admin Credentials**
   - **Username:** Your admin username
   - **Password:** Your admin password

3. **Click "Login as Admin"** button

4. **Success!** You'll be redirected to Admin Dashboard

---

### **🔧 How to Create an Admin Account**

#### **Method 1: Register as Admin** (If Enabled)
- URL: `http://127.0.0.1:8000/register/admin/`
- Fill in the registration form
- Select appropriate admin permissions

#### **Method 2: Using Django Superuser** (Terminal)
```bash
python manage.py createsuperuser
```
- Enter username, email, and password when prompted
- Access Django Admin: `http://127.0.0.1:8000/admin/`

#### **Method 3: Using Custom Command** (Terminal)
```bash
python manage.py make_superuser
```

---

### **⚙️ Features Available for Admins**

After logging in, admins can access:

#### **1. Admin Dashboard** 📊
- URL: `http://127.0.0.1:8000/dashboard-admin/`
- **Features:**
  - Overview of all scholarships
  - Total applications count
  - User statistics
  - Recent activities
  - Quick action buttons
  - System analytics

#### **2. Scholarship Management** 📚
- URL: `http://127.0.0.1:8000/scholarships/manage/`
- **Features:**
  - **View All Scholarships:** Complete list with details
  - **Add New Scholarship:** Create new scholarship entries
  - **Edit Scholarships:** Modify existing scholarship details
  - **Delete Scholarships:** Remove outdated scholarships
  - **Bulk Operations:** Manage multiple scholarships at once
  - **Filter & Search:** Find specific scholarships quickly

#### **3. Add New Scholarship** ➕
- URL: `http://127.0.0.1:8000/scholarship/add/`
- **Features:**
  - Complete scholarship form
  - Set eligibility criteria:
    - Minimum CGPA
    - Education level requirement
    - Category eligibility
    - Income criteria
    - Gender requirements
  - Upload scholarship documents
  - Set application deadlines
  - Define award amounts

#### **4. Edit Scholarship** ✏️
- URL: `http://127.0.0.1:8000/scholarship/edit/<id>/`
- **Features:**
  - Modify all scholarship fields
  - Update eligibility criteria
  - Change deadline dates
  - Update contact information

#### **5. Delete Scholarship** 🗑️
- URL: `http://127.0.0.1:8000/scholarship/delete/<id>/`
- **Features:**
  - Remove scholarships safely
  - Confirmation before deletion
  - Cascade handling of related applications

#### **6. Application Management** 📝
- URL: `http://127.0.0.1:8000/applications/manage/`
- **Features:**
  - View all applications
  - Filter by status (Pending/Approved/Rejected)
  - Sort by date, scholarship, or student
  - Bulk status updates
  - Export applications data

#### **7. Review Applications** 👁️
- URL: `http://127.0.0.1:8000/application/review/<id>/`
- **Features:**
  - View complete application details
  - Check student eligibility
  - Review submitted documents
  - **Approve Application:** Mark as approved
  - **Reject Application:** Mark as rejected with reason
  - **Add Comments:** Internal notes for tracking
  - **Request More Info:** Flag for additional documents

#### **8. User Management** 👥
- URL: `http://127.0.0.1:8000/users/manage/`
- **Features:**
  - View all registered users
  - See user profiles and details
  - Check user activity
  - Manage user permissions
  - Activate/deactivate accounts
  - Export user data

#### **9. Django Admin Panel** 🛠️
- URL: `http://127.0.0.1:8000/admin/`
- **Features (Full System Access):**
  - Database management
  - Direct model editing
  - User and group permissions
  - Site administration
  - Logs and history
  - Advanced filtering and search

---

## 📊 **FEATURES COMPARISON TABLE**

| Feature | Regular User | Admin |
|---------|-------------|-------|
| **Browse Scholarships** | ✅ Yes | ✅ Yes |
| **Search & Filter** | ✅ Yes | ✅ Yes |
| **View Details** | ✅ Yes | ✅ Yes |
| **Apply for Scholarships** | ✅ Yes | ❌ No |
| **Track Applications** | ✅ Own Only | ✅ All Users |
| **Profile Management** | ✅ Own Profile | ✅ View All |
| **AI Chatbot** | ✅ Yes | ✅ Yes |
| **Add Scholarships** | ❌ No | ✅ Yes |
| **Edit Scholarships** | ❌ No | ✅ Yes |
| **Delete Scholarships** | ❌ No | ✅ Yes |
| **Review Applications** | ❌ No | ✅ Yes |
| **Approve/Reject** | ❌ No | ✅ Yes |
| **User Management** | ❌ No | ✅ Yes |
| **System Analytics** | ❌ No | ✅ Yes |
| **Django Admin Access** | ❌ No | ✅ Yes |

---

## 🚀 **FIRST TIME SETUP**

### **For New Users:**

1. **Register an Account**
   - Go to: `http://127.0.0.1:8000/register/`
   - Complete the 3-step registration:
     - **Step 1:** Create account (email, phone, password)
     - **Step 2:** Verify OTP (6-digit code)
     - **Step 3:** Complete profile (academic & personal info)

2. **Login**
   - Use either Password or OTP method
   - Go to: `http://127.0.0.1:8000/login/`

3. **Complete Your Profile**
   - Go to Profile page
   - Fill in all required fields for better recommendations
   - Aim for 100% profile completion

4. **Start Browsing**
   - Explore available scholarships
   - Use filters to find relevant opportunities
   - Apply to scholarships you're eligible for

---

### **For New Admins:**

1. **Create Superuser Account** (Terminal)
   ```bash
   python manage.py createsuperuser
   ```

2. **Login to Django Admin**
   - Go to: `http://127.0.0.1:8000/admin/`
   - Use your superuser credentials

3. **Access Custom Admin Panel**
   - Login at: `http://127.0.0.1:8000/login/admin/`
   - Or go directly to: `http://127.0.0.1:8000/dashboard-admin/`

4. **Start Managing**
   - Add scholarships
   - Review applications
   - Manage users

---

## 🔒 **SECURITY TIPS**

### **For All Users:**
- ✅ Use a strong password (minimum 8 characters, mix of letters, numbers, symbols)
- ✅ Don't share your password with anyone
- ✅ Log out when using shared computers
- ✅ Verify the website URL before entering credentials
- ✅ Keep your email/phone number updated for OTP
- ✅ Enable "Remember Me" only on personal devices

### **For Admins:**
- ✅ Use an extra-strong password
- ✅ Never share admin credentials
- ✅ Always log out after admin tasks
- ✅ Monitor user activities regularly
- ✅ Keep sensitive data confidential
- ✅ Use two-factor authentication when possible

---

## 🆘 **TROUBLESHOOTING**

### **Can't Login?**
- ✅ Check your username/email is correct
- ✅ Verify your password (case-sensitive)
- ✅ Clear browser cache and cookies
- ✅ Try "Forgot Password" option
- ✅ Try OTP login instead

### **OTP Not Received?**
- ✅ Check spam/junk folder (for email)
- ✅ Verify your email/phone is correct
- ✅ Wait 1-2 minutes (delivery delay)
- ✅ Click "Resend OTP" after countdown
- ✅ Check your internet connection

### **Profile Issues?**
- ✅ Make sure all required fields are filled
- ✅ Use valid data formats (age, CGPA, etc.)
- ✅ Save your changes before navigating away
- ✅ Refresh the page if changes don't appear

### **Admin Access Issues?**
- ✅ Ensure you're using the admin login URL: `/login/admin/`
- ✅ Verify you have admin/superuser permissions
- ✅ Contact system administrator if locked out
- ✅ Check if your admin account is active

---

## 📞 **SUPPORT**

Need help? Contact:
- **Email:** support@ai-scholar.com
- **Phone:** +91-XXXX-XXXXXX
- **Chatbot:** Available 24/7 at `/chatbot/`

---

## 📅 **Quick Reference**

| Action | URL |
|--------|-----|
| User Registration | `/register/` |
| User Login | `/login/` |
| Admin Login | `/login/admin/` |
| User Dashboard | `/dashboard/` |
| Admin Dashboard | `/dashboard-admin/` |
| Profile | `/profile/` |
| Scholarships | `/scholarships/` |
| Chatbot | `/chatbot/` |
| Django Admin | `/admin/` |

---

**Last Updated:** December 31, 2025  
**Version:** 1.0  
**System:** AI-Scholar Platform
