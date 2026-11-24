# AI-Scholar Installation Guide

## Prerequisites

- Python 3.12 or higher
- pip (Python package manager)
- Git (optional, for version control)

## Step-by-Step Installation

### 1. System Requirements Check

Verify Python installation:
```bash
python --version
```

Expected output: Python 3.12.x or higher

### 2. Project Setup

Navigate to the project directory:
```bash
cd "c:\All Programing\TechKalaA\AI Scholarship web"
```

### 3. Install Dependencies

Install all required Python packages:
```bash
pip install -r requirements.txt
```

This will install:
- Django 4.2.23 (Web framework)
- Pillow 10.1.0 (Image processing)
- scikit-learn 1.7.1 (Machine learning)
- pandas 2.3.1 (Data analysis)
- numpy 1.26.4 (Numerical computing)
- joblib 1.5.1 (Model persistence)

### 4. Database Setup

Run database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Admin User

Create a superuser account for admin access:
```bash
python manage.py createsuperuser
```

Follow the prompts to set:
- Username
- Email address (optional)
- Password

### 6. Collect Static Files (Optional for development)

```bash
python manage.py collectstatic
```

### 7. Run Development Server

Start the Django development server:
```bash
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000/**

### 8. Access Admin Panel

Navigate to: **http://127.0.0.1:8000/admin/**

Login with your superuser credentials.

## Project Structure

```
AI Scholarship web/
├── ai_scholar/              # Django project configuration
│   ├── settings.py          # Project settings
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI configuration
│
├── scholar_app/             # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── urls.py              # App URL patterns
│   └── admin.py             # Admin configuration
│
├── frontend/                # Frontend assets
│   ├── templates/           # HTML templates
│   ├── css/                 # Stylesheets
│   └── js/                  # JavaScript files
│
├── ai_engine/               # AI/ML engine
│   ├── recommendation_model.py  # Recommendation algorithms
│   ├── chatbot.py           # Chatbot logic
│   └── models/              # Trained ML models
│
├── static/                  # Collected static files
├── media/                   # User uploads
├── docs/                    # Documentation
├── manage.py                # Django CLI tool
├── requirements.txt         # Python dependencies
└── README.md                # Project overview
```

## Troubleshooting

### Issue: Port already in use
```bash
# Use a different port
python manage.py runserver 8001
```

### Issue: Missing dependencies
```bash
# Reinstall all packages
pip install -r requirements.txt --force-reinstall
```

### Issue: Database locked
```bash
# Stop all running Django processes and restart
python manage.py runserver
```

## Next Steps

After installation:

1. **Configure settings** in `ai_scholar/settings.py`
2. **Create models** in `scholar_app/models.py`
3. **Design frontend** in `frontend/templates/`
4. **Implement AI engine** in `ai_engine/`
5. **Test the application** thoroughly

## Development Workflow

1. Make changes to code
2. Run migrations if models changed:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Test changes locally
4. Commit to version control

## Additional Resources

- Django Documentation: https://docs.djangoproject.com/
- Scikit-learn Documentation: https://scikit-learn.org/
- Project GitHub: [Add your repository URL]

## Support

For issues or questions, please refer to the project documentation or contact the development team.
