"""
Django settings for biocontainers-django project.

Generated by 'django-admin startproject' using Django 2.0.9.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from pymodm import connect

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$@#a_dvj6ra)#d_q9@87zm4d)xw4&dk^^sv8-q)q%h$cc7guz)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'rest_framework_swagger',
    'rest_framework',
    'rest_framework_mongoengine',
    'mongoengine.django.mongo_auth',
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

ROOT_URLCONF = 'restapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'biocontainers-django.restapi.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# # We define 2 Mongo databases - default and test
# MONGODB_DATABASES = {
#     "default": {
#         "NAME": "testDB",
#         "HOST": "localhost",
#         "PORT": 27017,
#         'USER': 'admin',
#         'PASSWORD': 'admin01',
#         'AUTH_SOURCE': 'admin',
#     },
#
#     "test": {
#         "NAME": "testDB",
#         "HOST": "localhost",
#         "PORT": 27017,
#     }
# }


# def is_test():
#     """
#     Checks, if we're running the server for real or in unit-test.
#     We might need a better implementation of this function.
#     """
#     if 'test' in sys.argv or 'testserver' in sys.argv:
#         print("Using a test mongo database")
#         return True
#     else:
#         print("Using a default mongo database")
#         return False


# if is_test():
#     db = 'test'
# else:
#     db = 'default'

# # establish connection with default or test database, depending on the management command, being run
# # # note that this connection syntax is correct for mongoengine0.9-, but mongoengine0.10+ introduced slight changes
# # mongoengine.connect(
# #     db=MONGODB_DATABASES[db]['NAME'],
# #     host=MONGODB_DATABASES[db]['HOST'],
# #     port=MONGODB_DATABASES[db]['PORT'],
# #     username=MONGODB_DATABASES[db]['USER'],
# #     password=MONGODB_DATABASES[db]['PASSWORD']
# # )

# mongoengine connection
# _MONGODB_USER = 'admin'
# _MONGODB_PASSWD = 'admin01'
# _MONGODB_HOST = 'localhost'
# _MONGODB_NAME = 'testdb'
_MONGO_URI='mongodb://localhost:27017/testdb'
connect(_MONGO_URI)

# This is a dummy django model. It's just a crutch to keep django content,
# while all the real functionality is associated with MONGOENGINE_USER_DOCUMENT
# AUTH_USER_MODEL = 'mongo_auth.MongoUser'

# MONGOENGINE_USER_DOCUMENT = 'mongoengine.django.auth.User'
#
# # Don't confuse Django's AUTHENTICATION_BACKENDS with DRF's AUTHENTICATION_CLASSES!
# AUTHENTICATION_BACKENDS = (
#     #'mongoengine.django.auth.MongoEngineBackend',
#     'django.contrib.auth.backends.ModelBackend'
# )

# AUTH_USER_MODEL = 'mongo_auth.MongoUser'
#
# MONGOENGINE_USER_DOCUMENT = 'users.models.User'
#
# # Don't confuse Django's AUTHENTICATION_BACKENDS with DRF's AUTHENTICATION_CLASSES!
# AUTHENTICATION_BACKENDS = (
#     'mongoengine.django.auth.MongoEngineBackend',
#     #'django.contrib.auth.backends.ModelBackend'
# )


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

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

SWAGGER_SETTINGS = {
    "exclude_namespaces": [], # List URL namespaces to ignore
    "api_version": '0.1',  # Specify your API's version
    "api_path": "/api/",  # Specify the path to your API not a root level
    "enabled_methods": [  # Specify which methods to enable in Swagger UI
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    "api_key": '', # An API key
    "is_authenticated": False,  # Set to True to enforce user authentication,
    "is_superuser": False,  # Set to True to enforce admin only access
    'info': {
        'contact': 'apiteam@wordnik.com',
        'description': 'This is a sample server Petstore server. '
                       'You can find out more about Swagger at '
                       '<a href="http://swagger.wordnik.com">'
                       'http://swagger.wordnik.com</a> '
                       'or on irc.freenode.net, #swagger. '
                       'For this sample, you can use the api key '
                       '"special-key" to test '
                       'the authorization filters',
        'license': 'Apache 2.0',
        'licenseUrl': 'http://www.apache.org/licenses/LICENSE-2.0.html',
        'termsOfServiceUrl': 'http://helloreverb.com/terms/',
        'title': 'Swagger Sample App',
    }
}