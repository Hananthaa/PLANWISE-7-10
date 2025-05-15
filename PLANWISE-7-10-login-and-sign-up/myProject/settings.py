from pathlib import Path
import os

# Base directory path for your project
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret Key for your project (keep this secret in production)
SECRET_KEY = 'django-insecure-ah4_8j3c8^05p-=t&ve6ppu_63iii_up1u&m=6vbqno3*2&((@'

# Debug mode (set to False in production)
DEBUG = True

# Allowed hosts (set this in production)
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']  # Add valid hosts for production

# Installed apps include your app, authentication, and CKEditor
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myApp',  # Your application
    'django_ckeditor_5',  # CKEditor app
]

# Middleware to handle requests and responses
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL configuration for your project
ROOT_URLCONF = 'myProject.urls'

# Template settings for rendering HTML pages
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Add this line
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application entry point
WSGI_APPLICATION = 'myProject.wsgi.application'

# Database configuration (SQLite for development)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # SQLite database in your base directory
    }
}

# Password validation settings
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Localization settings (time zone, language)
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files settings (CSS, JavaScript, images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # Directory for additional static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Collected static files for production

# Media files settings (uploads, images, etc.)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# CKEditor settings (for rich text editor in forms)
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link', 'undo', 'redo', 'imageUpload'],
        'language': 'en',
    }
}

# Authentication settings
LOGIN_REDIRECT_URL = '/'  # Redirect after successful login
LOGOUT_REDIRECT_URL = '/'  # Redirect after logging out

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email backend (for development, emails will print in the console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Optional: Session settings to control session expiration
SESSION_COOKIE_AGE = 3600  # Session expiration after 1 hour
SESSION_COOKIE_SECURE = False  # Set to True for production (HTTPS)
CSRF_COOKIE_SECURE = False  # Set to True for production (HTTPS)

LOGIN_URL = '/login/'
