"""
Django settings for oar project.

Generated by 'django-admin startproject' using Django 2.0.9.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import requests

from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'secret')

# Set environment
ENVIRONMENT = os.getenv('DJANGO_ENV', 'Development')
VALID_ENVIRONMENTS = ('Production', 'Staging', 'Development')
if ENVIRONMENT not in VALID_ENVIRONMENTS:
    raise ImproperlyConfigured(
        'Invalid ENVIRONMENT provided, must be one of {}'
        .format(VALID_ENVIRONMENTS))

# A non-empty value of BATCH_MODE signals that we will only be running batch
# processing management commands
BATCH_MODE = os.getenv('BATCH_MODE', '')

LOGLEVEL = os.getenv('DJANGO_LOG_LEVEL', 'INFO')

GIT_COMMIT = os.getenv('GIT_COMMIT', 'UNKNOWN')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (ENVIRONMENT == 'Development')

ALLOWED_HOSTS = [
    '.openapparel.org'
]

if ENVIRONMENT == 'Development':
    ALLOWED_HOSTS.append('localhost')
    ALLOWED_HOSTS.append('django')

if ENVIRONMENT in ['Production', 'Staging'] and BATCH_MODE == '':
    # Within EC2, the Elastic Load Balancer HTTP health check will use the
    # target instance's private IP address for the Host header.
    #
    # The following steps lookup the current instance's private IP address
    # (via the EC2 instance metadata URL) and add it to the Django
    # ALLOWED_HOSTS configuration so that health checks pass.
    #
    # Beginning with version 1.17.0 of the Amazon ECS container agent,
    # tasks that use the awsvpc network mode will have to use the
    # ECS Task Metadata endpoint.

    response = requests.get('http://169.254.170.2/v2/metadata')
    if response.ok:
        response = response.json()

        for container in response['Containers']:
            for network in container['Networks']:
                for addr in network['IPv4Addresses']:
                    ALLOWED_HOSTS.append(addr)
    else:
        raise ImproperlyConfigured('Unable to fetch instance metadata')

    # Ensure Django knows to determine whether an inbound request was
    # made over HTTPS by the ALBs HTTP_X_FORWARDED_PROTO header.
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_gis',
    'rest_framework_swagger',
    'rest_auth',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_auth.registration',
    'watchman',
    'simple_history',
    'waffle',
    'api',
    'web',
    'ecsmanage',
]

# For allauth
SITE_ID = 1
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_ADAPTER = "api.adapters.OARUserAccountAdapter"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
ACCOUNT_EMAIL_SUBJECT_PREFIX = ''

AUTH_USER_MODEL = 'api.User'

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'api.serializers.UserSerializer',
    'PASSWORD_RESET_SERIALIZER': 'api.serializers.UserPasswordResetSerializer',
    'PASSWORD_RESET_CONFIRM_SERIALIZER': 'api.serializers.UserPasswordResetConfirmSerializer',
}

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'rollbar.contrib.django_rest_framework.post_exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'api.permissions.IsAuthenticatedOrWebClient',
    ),
    'DEFAULT_PAGINATION_CLASS': 'api.pagination.PageAndSizePagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
        },
    },
    'doc_expansion': 'list',
    'info': {
        'description': 'Open Apparel Registry API',
        'license': 'MIT',
        'licenseUrl': 'https://github.com/open-apparel-registry/open-apparel-registry/blob/develop/LICENSE',  # noqa
        'title': 'Open Apparel Registry API',
    },
    'USE_SESSION_AUTH': False,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'spa.middleware.SPAMiddleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddlewareExcluding404',
    'simple_history.middleware.HistoryRequestMiddleware',
    'waffle.middleware.WaffleMiddleware',
    'api.middleware.RequestLogMiddleware',
    'api.middleware.RequestMeterMiddleware',
]

ROOT_URLCONF = 'oar.urls'

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

WSGI_APPLICATION = 'oar.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT')
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

# User model
# https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#substituting-a-custom-user-model

AUTH_USER_MODEL = 'api.User'

# Api Limits
API_FREE_REQUEST_LIMIT = 50

# Logging
# https://docs.djangoproject.com/en/2.1/topics/logging/

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Email
# https://docs.djangoproject.com/en/2.0/topics/email

AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', 'eu-west-1')

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django_amazon_ses.EmailBackend'

DEFAULT_FROM_EMAIL = os.getenv(
    'DEFAULT_FROM_EMAIL', 'noreply@staging.openapparel.org')

NOTIFICATION_EMAIL_TO = os.getenv(
    'NOTIFICATION_EMAIL_TO', 'notification@example.com')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_STORAGE = 'spa.storage.SPAStaticFilesStorage'

# Watchman
# https://github.com/mwarkentin/django-watchman

WATCHMAN_ERROR_CODE = 503
WATCHMAN_CHECKS = (
    'watchman.checks.databases',
    'api.checks.gazetteercache'
)

# django-ecsmanage
# https://github.com/azavea/django-ecsmanage

ECSMANAGE_ENVIRONMENTS = {
    'default': {
        'TASK_DEFINITION_NAME': 'StagingAppCLI',
        'CONTAINER_NAME': 'django',
        'CLUSTER_NAME': 'ecsStagingCluster',
        'LAUNCH_TYPE': 'FARGATE',
        'PLATFORM_VERSION': '1.4.0',
        'SECURITY_GROUP_TAGS': {
            'Name': 'sgAppEcsService',
            'Environment': 'Staging',
            'Project': 'OpenApparelRegistry'
        },
        'SUBNET_TAGS': {
            'Name': 'PrivateSubnet',
            'Environment': 'Staging',
            'Project': 'OpenApparelRegistry'
        },
        'AWS_REGION': 'eu-west-1',
    },
    'production': {
        'TASK_DEFINITION_NAME': 'ProductionAppCLI',
        'CONTAINER_NAME': 'django',
        'CLUSTER_NAME': 'ecsProductionCluster',
        'LAUNCH_TYPE': 'FARGATE',
        'PLATFORM_VERSION': '1.4.0',
        'SECURITY_GROUP_TAGS': {
            'Name': 'sgAppEcsService',
            'Environment': 'Production',
            'Project': 'OpenApparelRegistry'
        },
        'SUBNET_TAGS': {
            'Name': 'PrivateSubnet',
            'Environment': 'Production',
            'Project': 'OpenApparelRegistry'
        },
        'AWS_REGION': 'eu-west-1',
    }
}

# Application settings
MAX_UPLOADED_FILE_SIZE_IN_BYTES = 5242880
TILE_CACHE_MAX_AGE_IN_SECONDS = 60 * 60 * 24 * 365 # 1 year. Also in deployment/terraform/cdn.tf  # NOQA

GOOGLE_SERVER_SIDE_API_KEY = os.getenv('GOOGLE_SERVER_SIDE_API_KEY')
if GOOGLE_SERVER_SIDE_API_KEY is None:
    raise ImproperlyConfigured(
        'Invalid GOOGLE_SERVER_SIDE_API_KEY provided, must be set')

if not DEBUG:
    ROLLBAR = {
        'access_token': os.getenv('ROLLBAR_SERVER_SIDE_ACCESS_TOKEN'),
        'environment': ENVIRONMENT.lower(),
        'root': BASE_DIR,
        'suppress_reinit_warning': True,
    }
    import rollbar
    rollbar.init(**ROLLBAR)

OAR_CLIENT_KEY = os.getenv('OAR_CLIENT_KEY')
if OAR_CLIENT_KEY is None:
    raise ImproperlyConfigured(
        'Invalid OAR_CLIENT_KEY provided, must be set')
