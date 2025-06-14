from pathlib import Path
import os

import os
import dj_database_url


# Base directory path for your project
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret Key for your project (keep this secret in production)
SECRET_KEY = 'django-insecure-ah4_8j3c8^05p-=t&ve6ppu_63iii_up1u&m=6vbqno3*2&((@'

# Debug mode (set to False in production)
DEBUG = True

# Allowed hosts (set this in production)
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myApp',  # Your application
    'django_ckeditor_5',  # CKEditor app
    'django_extensions',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',


]

# Root URL configuration
ROOT_URLCONF = 'myProject.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# WSGI application
WSGI_APPLICATION = 'myProject.wsgi.application'

# Database (SQLite for development)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
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

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files (uploads, images, etc.)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# CKEditor settings
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link', 'undo', 'redo', 'imageUpload'],
        'language': 'en',
    }
}

# Authentication settings
LOGIN_REDIRECT_URL = '/home3/'   # Redirect to dashboard after login
LOGOUT_REDIRECT_URL = '/login/'      # Redirect to login page after logout

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email backend (prints to console for development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Session settings
SESSION_COOKIE_AGE = 3600  # 1 hour
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
