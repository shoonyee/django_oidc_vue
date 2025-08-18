import os
import sys
from pathlib import Path
from decouple import config

# Try to import database drivers and configure them if available
try:
    import pymysql
    pymysql.install_as_MySQLdb()
    print("🐬 Using PyMySQL as MySQL driver")
except ImportError:
    print("🐬 MySQL driver not available")

try:
    import psycopg2
    print("🐘 PostgreSQL driver (psycopg2) available")
except ImportError:
    print("🐘 PostgreSQL driver not available")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Global application mode
MODE = config('MODE', default='LOCAL')  # LOCAL or PROD

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = [
    'localhost', 
    '127.0.0.1', 
    '.umich.edu',
]

# Application definition - conditional based on MODE
if MODE == 'PROD':
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',
        'corsheaders',
        'mozilla_django_oidc',
        'api',
    ]
    print("🔐 OIDC app enabled for production")
else:
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',
        'corsheaders',
        'api',
    ]
    print("🚫 OIDC app disabled for local development")

# Middleware configuration - conditional based on MODE
if MODE == 'PROD':
    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
    ]
    print("🔐 CSRF protection enabled for production")
else:
    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        # 'django.middleware.csrf.CsrfViewMiddleware',  # Disabled for local development
        'django.contrib.auth.middleware.AuthenticationMiddleware',
    ]
    print("🚫 CSRF protection disabled for local development")

# Add OIDC middleware only in production mode
if MODE == 'PROD':
    MIDDLEWARE.append('mozilla_django_oidc.middleware.SessionRefresh')
    print("🔐 OIDC middleware enabled")
else:
    print("🚫 OIDC middleware disabled")

MIDDLEWARE.extend([
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
])

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'

# Database
# Get database configuration from environment variables
DB_ENGINE = config('DB_ENGINE', default='sqlite3')
DB_NAME = config('DB_NAME', default='db.sqlite3')
DB_USER = config('DB_USER', default='')
DB_PASSWORD = config('DB_PASSWORD', default='')
DB_HOST = config('DB_HOST', default='')
DB_PORT = config('DB_PORT', default='')

if DB_ENGINE == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': DB_NAME,
            'USER': DB_USER,
            'PASSWORD': DB_PASSWORD,
            'HOST': DB_HOST,
            'PORT': DB_PORT,
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }
elif DB_ENGINE == 'postgresql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': DB_NAME,
            'USER': DB_USER,
            'PASSWORD': DB_PASSWORD,
            'HOST': DB_HOST,
            'PORT': DB_PORT,
        }
    }
else:
    # Default to SQLite
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

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8088",
    "http://127.0.0.1:8088",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

CORS_ALLOW_CREDENTIALS = True

# CSRF settings for local development
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8088",
    "http://127.0.0.1:8088",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

# Allow credentials in CSRF
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = False  # Allow JavaScript access for CSRF token
CSRF_USE_SESSIONS = False  # Use cookies instead of sessions for CSRF

# REST Framework settings - conditional based on MODE
if MODE == 'PROD':
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.SessionAuthentication',
            'mozilla_django_oidc.contrib.drf.OIDCAuthentication',
        ],
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_RENDERER_CLASSES': [
            'rest_framework.renderers.JSONRenderer',
        ],
    }
    print("🔐 OIDC authentication enabled in REST framework")
else:
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'api.authentication.NoCSRFSessionAuthentication',
        ],
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_RENDERER_CLASSES': [
            'rest_framework.renderers.JSONRenderer',
        ],
    }
    print("🚫 OIDC authentication disabled in REST framework")
    print("🚫 CSRF protection disabled in REST framework")

# OIDC Authentication settings - conditional based on MODE
if MODE == 'PROD':
    # Production: U-M Shibboleth OIDC
    OIDC_RP_CLIENT_ID = config('OIDC_CLIENT_ID', default='your-app-client-id')
    OIDC_RP_CLIENT_SECRET = config('OIDC_CLIENT_SECRET', default='your-app-client-secret')
    OIDC_RP_SIGN_ALGO = 'RS256'
    OIDC_OP_AUTHORIZATION_ENDPOINT = config('OIDC_AUTHORIZATION_ENDPOINT', default='https://shibboleth.umich.edu/idp/profile/oidc/authorize')
    OIDC_OP_TOKEN_ENDPOINT = config('OIDC_TOKEN_ENDPOINT', default='https://shibboleth.umich.edu/idp/profile/oidc/token')
    OIDC_OP_USER_ENDPOINT = config('OIDC_USER_ENDPOINT', default='https://shibboleth.umich.edu/idp/profile/oidc/userinfo')
    OIDC_OP_JWKS_ENDPOINT = config('OIDC_JWKS_ENDPOINT', default='https://shibboleth.umich.edu/oidc/keyset.jwk')
    
    # OIDC Settings
    OIDC_VERIFY_SSL = True
    OIDC_CREATE_USER = True
    OIDC_USE_USERNAME = False
    OIDC_UPDATE_USER = True
    OIDC_USERNAME_ALGO = 'mozilla_django_oidc.utils.generate_username'
    OIDC_STORE_ACCESS_TOKEN = True
    OIDC_STORE_ID_TOKEN = True
    OIDC_STORE_REFRESH_TOKEN = True
    OIDC_RP_SCOPES = 'openid email profile eduperson edumember'
    OIDC_RP_IDP_SIGN_KEY = None
    
    # U-M specific OIDC settings
    OIDC_OP_ISSUER = 'https://shibboleth.umich.edu'
    OIDC_RP_SIGN_ALGO = 'RS256'  # Supported by U-M
    OIDC_VERIFY_SSL = True
    
    print("🚀 Running in PRODUCTION mode with U-M Shibboleth OIDC")
else:
    # Local: Disable OIDC, use mock authentication
    print("🔧 Running in LOCAL mode with mock authentication")
    print("📝 Use /api/auth/mock_login/ for testing authentication")
    print("🔐 Admin interface available at /admin/")
    print("🚫 OIDC app and authentication classes disabled")
    print("🔑 Using only ModelBackend for authentication")

# Authentication backends - conditional based on MODE
if MODE == 'PROD':
    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'mozilla_django_oidc.auth.OIDCAuthenticationBackend',
    )
    print("🔐 OIDC authentication backend enabled")
else:
    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
    )
    print("🔑 Using only ModelBackend for authentication")

# Login/Logout URLs - conditional based on MODE
if MODE == 'PROD':
    LOGIN_URL = '/oidc/authenticate/'
    LOGIN_REDIRECT_URL = '/'
    LOGOUT_REDIRECT_URL = '/'
else:
    LOGIN_URL = '/admin/login/'
    LOGIN_REDIRECT_URL = '/'
    LOGOUT_REDIRECT_URL = '/'

# Session settings - conditional based on MODE
if MODE == 'PROD':
    # Production: OIDC session settings
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_EXPIRE_AT_BROWSER_CLOSE = False
    SESSION_COOKIE_AGE = 3600 * 24 * 7  # 7 days
    
    # OIDC callback settings
    OIDC_CALLBACK_CLASS = 'mozilla_django_oidc.views.OIDCAuthenticationCallbackView'
else:
    # Local: Simple session settings
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_EXPIRE_AT_BROWSER_CLOSE = False
    SESSION_COOKIE_AGE = 3600 * 24 * 7  # 7 days

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# Print final configuration summary
print(f"\n🎯 Configuration Summary:")
print(f"   Mode: {MODE}")
print(f"   Debug: {DEBUG}")
print(f"   Installed Apps: {len(INSTALLED_APPS)} apps")
print(f"   Middleware: {len(MIDDLEWARE)} components")
print(f"   Auth Backends: {len(AUTHENTICATION_BACKENDS)} backends")
print(f"   REST Auth Classes: {len(REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'])} classes")
print(f"   Database Engine: {DATABASES['default']['ENGINE']}")
print(f"   Database Name: {DATABASES['default']['NAME']}")
print("")

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # For development - prints to console
# For production, use SMTP:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'  # or your SMTP server
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@gmail.com'
# EMAIL_HOST_PASSWORD = 'your-app-password'

# Default email settings
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@example.com')
ADMIN_EMAILS = config('ADMIN_EMAILS', default='admin@example.com').split(',')

print(f"📧 Email backend: {EMAIL_BACKEND}")
print(f"📧 From email: {DEFAULT_FROM_EMAIL}")
print(f"📧 Admin emails: {ADMIN_EMAILS}")
print("")
