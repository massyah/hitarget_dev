"""
Django settings for hitargetMVP project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from django.core.urlresolvers import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!x)ed^v_9v^bx^us0ac*6fk(edxi(vplyd54++yg84ds@if4uo'

# SECURITY WARNING: don't run with debug turned on in production!
# SETTING = "PROD"
# SETTING = "PYANYWHERE"
# SETTING = "DEBUG"
SETTING = "OVHPROD"



# LOGGER setup
import os

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


ALLOWED_HOSTS = ['100doutes.pythonanywhere.com', '127.0.0.1','192.168.1.8']

LOGIN_REDIRECT_URL = reverse_lazy("dashboard")
LOGIN_URL = reverse_lazy("login")
LOGOUT_URL = reverse_lazy("logout")

# Application definition

INSTALLED_APPS = [
    'data_management',
    'hitarget',
    'account',
    'bootstrap3',
    'crispy_forms',
    'django.contrib.postgres',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hitargetMVP.urls'

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

WSGI_APPLICATION = 'hitargetMVP.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hitarget',
        'USER': 'django_hitarget',
        'PASSWORD': 'li8oph6aw8ulk7en6cyp7vak7ur3yet0bum6nom2cip3nird4y',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


LANGUAGE_CODE = 'fr-FR'
USE_L10N = True

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

if SETTING == "DEBUG":
    # STATIC_URL = 'http://127.0.0.1:8000/static/'
    # STATIC_ROOT = '/Users/hayssam/Documents/Web_development/hitarget_dev/static'
    STATIC_URL = '/static/'
    DEBUG = True
    print("Runing in DEBUG mode")
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

    pass

elif SETTING == "PYANYWHERE":
    STATIC_URL = '/static/'
    STATIC_ROOT = '/home/100doutes/hitarget_dev/static/static/'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = '/home/100doutes/hitarget_dev/static/media/'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
elif SETTING == "OVHPROD":
    # STATIC_URL = '/static/'
    STATIC_ROOT = '/home/hayssam/hitarget_dev/static/static/'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

else:
    STATIC_URL = '/static/'
