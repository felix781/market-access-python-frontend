"""
Django settings for market_access_python_frontend project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

from django.utils.log import DEFAULT_LOGGING

from environ import Env
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


ROOT_DIR = os.path.abspath(os.path.dirname(__name__))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV_FILE = os.path.join(BASE_DIR, ".env")

if os.path.exists(ENV_FILE):
    Env.read_env(ENV_FILE)

env = Env(
    DEBUG=(bool, False)
)

# Load PaaS Service env vars
VCAP_SERVICES = env.json('VCAP_SERVICES', default={})

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
# Application definition

BASE_APPS = [
    # apps that need to load first
    'whitenoise.runserver_nostatic',
]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.forms',
]

THIRD_PARTY_APPS = [
    "django_extensions",
    'compressor',
    'sass_processor',
]

LOCAL_APPS = [
    'barriers',
    'core',
    'reports',
    'users',
]

INSTALLED_APPS = BASE_APPS + DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'users.middleware.SSOMiddleware',
]

ROOT_URLCONF = 'config.urls'

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

SESSION_ENGINE = "users.sessions"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(ROOT_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'utils.context_processors.user_scope',
                'django_settings_export.settings_export',
            ],
            'builtins':[
                'core.templatetags.govuk_forms'
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": env.db("DATABASE_URL"),
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ROOT_DIR, "staticfiles")
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

COMPRESS_ROOT = os.path.join(ROOT_DIR, "core/static/")
COMPRESS_FILTERS = {
    'css': [
        'compressor.filters.css_default.CssAbsoluteFilter',
        'compressor.filters.cssmin.rCSSMinFilter',
    ],
    'js': [
        'compressor.filters.jsmin.JSMinFilter',
    ]
}


TRUSTED_USER_TOKEN = 'ssobypass'

METADATA_CACHE_TIME = "10600"
MOCK_METADATA = False

# CACHE / REDIS
# Try to read from PaaS service env vars first
REDIS_DB = env.int("REDIS_DB", default=4)
if "redis" in VCAP_SERVICES:
    REDIS_URI = VCAP_SERVICES["redis"][0]["credentials"]["uri"]
else:
    REDIS_URI = env("REDIS_URI")
REDIS_URI = f"{REDIS_URI}/{REDIS_DB}"

# Market access API
MARKET_ACCESS_API_URI = env("MARKET_ACCESS_API_URI")
MARKET_ACCESS_API_HAWK_ID = env("MARKET_ACCESS_API_HAWK_ID")
MARKET_ACCESS_API_HAWK_KEY = env("MARKET_ACCESS_API_HAWK_KEY")

SETTINGS_EXPORT = [
    'DJANGO_ENV',
    'MAX_WATCHLIST_LENGTH',
    'DATAHUB_DOMAIN',
]

SSO_CLIENT = env("SSO_CLIENT")
SSO_SECRET = env("SSO_SECRET")
SSO_API_URI = env("SSO_API_URI")
SSO_API_TOKEN = env("SSO_API_TOKEN")
SSO_AUTHORIZE_URI = env("SSO_AUTHORIZE_URI")
SSO_BASE_URI = env("SSO_BASE_URI")
SSO_TOKEN_URI = env("SSO_TOKEN_URI")
SSO_MOCK_CODE = env("SSO_MOCK_CODE", default=None)
OAUTH_PARAM_LENGTH = env("OAUTH_PARAM_LENGTH", default=75)

DATAHUB_DOMAIN = env("DATAHUB_DOMAIN", default="https://www.datahub.trade.gov.uk")
DATAHUB_URL = env("DATAHUB_URL")
DATAHUB_HAWK_ID = env("DATAHUB_HAWK_ID")
DATAHUB_HAWK_KEY = env("DATAHUB_HAWK_KEY")

FILE_MAX_SIZE = env.int("FILE_MAX_SIZE", default=(5 * 1024 * 1024))
FILE_SCAN_MAX_WAIT_TIME = env.int("FILE_SCAN_MAX_WAIT_TIME", default=30000)
FILE_SCAN_STATUS_CHECK_INTERVAL = env.int(
    "FILE_SCAN_STATUS_CHECK_INTERVAL",
    default=500
)
ALLOWED_FILE_TYPES = env.list("ALLOWED_FILE_TYPES", default=["text/csv", "image/jpeg"])

API_RESULTS_LIMIT = env.int('API_RESULTS_LIMIT', default=100)
MAX_WATCHLIST_LENGTH = env.int('MAX_WATCHLIST_LENGTH', default=3)
MAX_WATCHLIST_NAME_LENGTH = env.int('MAX_WATCHLIST_NAME_LENGTH', default=25)

# Logging
# ============================================
DJANGO_LOG_LEVEL = env("DJANGO_LOG_LEVEL", default="info").upper()
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "[%(asctime)s] %(name)s %(levelname)5s - %(message)s"
        },
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[%(asctime)s] %(message)s",
        },
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "console"},
        "django.server": DEFAULT_LOGGING['handlers']['django.server']

    },
    "loggers": {
        # default for all undefined Python modules
        '': {
            'level': DJANGO_LOG_LEVEL,
            'handlers': ['console'],
        },
        # application code
        "app": {
            "level": DJANGO_LOG_LEVEL,
            "handlers": ["console"],
            "propagate": True,
        },
        # Default runserver request logging
        'django.server': DEFAULT_LOGGING['loggers']['django.server'],
    },
}


# Google Analytics
GA_ENABLED = env('GA_ENABLED', default=None)
GA_ID = env('GA_ID', default=None)

if not DEBUG:
    sentry_sdk.init(
        dsn=env('SENTRY_DSN'),
        environment=env('SENTRY_ENVIRONMENT'),
        integrations=[
            DjangoIntegration(),
        ],
    )
