import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key-here')
JWT_ACCESS_TOKEN_LIFETIME= int(os.getenv('JWT_ACCESS_TOKEN_LIFETIME', 86400))
DEBUG = True
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost').split(',')
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'person',
    'post',
    'alumnifund',
    'corsheaders',
    'rest_framework.authtoken',
    'django.contrib.sites',  # Required for allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

DATABASES = {
    'default':{
        'ENGINE' : 'django.db.backends.postgresql_psycopg2',
        'NAME' : 'postgres',
        'HOST' : os.environ.get('SUPABASE_HOST'),
        'PASSWORD': os.environ.get('SUPABASE_PW'),
        'USER': os.environ.get('SUPABASE_USER'),
        'PORT': 6543,
    }
}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),  # Set access token lifetime to 1 day
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # Optional: Set refresh token lifetime
}
# Configure User model
AUTH_USER_MODEL = 'person.User'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Required for admin
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Required for admin
    'django.contrib.messages.middleware.MessageMiddleware',  # Required for admin
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'allauth.account.middleware.AccountMiddleware'
    # ... other middleware
]
ROOT_URLCONF = 'connect.urls'
SECRET_KEY = 'your-secret-key-here'
DEBUG = True
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# For development only
CORS_ALLOW_ALL_ORIGINS = True  # Don't use in production 

# Add the site ID
SITE_ID = 1

# Configure authentication backends
AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Configure allauth settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"  # Change to "mandatory" if you want email verification
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False  # Optional: Disable username requirement
LOGIN_REDIRECT_URL = '/'  # Redirect URL after login 

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '211118@iiitt.ac.in')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'surajpura')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', '211118@iiitt.ac.in') 
EMAIL_HOST_PASSWORD = "jlsd aokm wkfk dyjq"