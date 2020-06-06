"""
Django settings for pepro project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

from dotenv import load_dotenv, find_dotenv
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

def get_env_value(env_variable, which_env_var):
    try:
      	return os.environ[env_variable]
    except KeyError:
        error_msg = 'Set the environment %s variable' %which_env_var
        raise ImproperlyConfigured(error_msg)


SECRET_KEY = os.environ.get('PEPro_SECRET_KEY')
# SECRET_KEY = get_env_value('PEPro_SECRET_KEY', 'SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.environ.get("DEBUG") in ("TRUE", "True", "1") else False

# ALLOWED_HOSTS = [
#         "127.0.0.1",
#         "localhost",
#         "pepro-320.herokuapp.com",
# ]
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'homepage',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Simplified static file serving.
    # https://warehouse.python.org/project/whitenoise/
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'pepro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + '/templates/',],
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

WSGI_APPLICATION = 'pepro.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': get_env_value('PEPro_DB_NAME', 'NAME'),
#         'USER': get_env_value('PEPro_DB_USER', 'USER'),
#         'PASSWORD': get_env_value('PEPro_DB_PASSWORD', 'PASSWORD'),
#         'HOST': get_env_value('PEPro_DB_HOST', 'HOST'),
#         'PORT': get_env_value('PEPro_DB_PORT', 'PORT'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('PEPro_DB_NAME', 'NAME'),
        'USER': os.environ.get('PEPro_DB_USER', 'USER'),
        'PASSWORD': os.environ.get('PEPro_DB_PASSWORD', 'PASSWORD'),
        'HOST': os.environ.get('PEPro_DB_HOST', 'HOST'),
        'PORT': os.environ.get('PEPro_DB_PORT', 'PORT'),
    }
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



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# gzip functionality 
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

'''
Uncomment
FOR SSL-DB-Deployment purpose
'''
# if os.getcwd() == '/app':
#     import dj_database_url
#     db_from_env = dj_database_url.config(conn_max_age=500)
#     DATABASES['default'].update(db_from_env)
#     #Honor the 'X-forwarded-Proto' header for request.is_secure().
#     SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

#     #Allow all host headers
#     ALLOWED_HOSTS = ['pepro-320.herokuapp.com']
#     DEBUG = True

#     #Static asset configuration
#     BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

'''
Uncomment
Heroku deloyment
'''
# import django_heroku
# django_heroku.settings(locals())

'''
Uncomment
Auth0 Login
'''
# ENV_FILE = find_dotenv()
# if ENV_FILE:
#     load_dotenv(ENV_FILE)

# # SOCIAL AUTH AUTH0 BACKEND CONFIG
# SOCIAL_AUTH_TRAILING_SLASH = False
# SOCIAL_AUTH_AUTH0_KEY = os.environ.get('AUTH0_CLIENT_ID')
# SOCIAL_AUTH_AUTH0_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')
# SOCIAL_AUTH_AUTH0_SCOPE = [
#     'openid',
#     'profile',
#     'email'
# ]
# SOCIAL_AUTH_AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
# AUDIENCE = None
# if os.environ.get('AUTH0_AUDIENCE'):
#     AUDIENCE = os.environ.get('AUTH0_AUDIENCE')
# else:
#     if SOCIAL_AUTH_AUTH0_DOMAIN:
#         AUDIENCE = 'https://' + SOCIAL_AUTH_AUTH0_DOMAIN + '/userinfo'
# if AUDIENCE:
#     SOCIAL_AUTH_AUTH0_AUTH_EXTRA_ARGUMENTS = {'audience': AUDIENCE}
# AUTHENTICATION_BACKENDS = {
#     'auth0login.auth0backend.Auth0',
#     'django.contrib.auth.backends.ModelBackend'
# }


# LOGIN_URL = '/login/auth0'
# LOGIN_REDIRECT_URL = '/dashboard'

