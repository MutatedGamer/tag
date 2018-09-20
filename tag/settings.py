"""
Django settings for tag project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from django.contrib.messages import constants as message_constants

MESSAGE_TAGS = {message_constants.ERROR: 'alert-danger', message_constants.SUCCESS: 'alert-success'}

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

with open('tag/secret_key.txt') as f:
	SECRET_KEY = f.read().strip()

with open('tag/facebook_appid.txt') as f:
	SOCIAL_AUTH_FACEBOOK_KEY = f.read().strip()

with open('tag/facebook_secret.txt') as f:
	SOCIAL_AUTH_FACEBOOK_SECRET = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['.elasticbeanstalk.com', '127.0.0.1', 'localhost', 'tag.mit.edu']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'social_django',
	'users.apps.UsersConfig',
	'main.apps.MainConfig',
	'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'tag.urls'

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
				'social_django.context_processors.backends',
				'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'tag.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

if 'RDS_HOSTNAME' in os.environ:
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.sqlite3',
			'NAME':  'db.sqlite3',
		}
	}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',

    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_friends',]

SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
	'fields': 'id, name, email',
}


SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
	'users.views.save_profile',
)

AUTH_USER_MODEL = 'users.CustomUser' # new
SOCIAL_AUTH_USER_MODEL = 'users.CustomUser'

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'index'

# Force https redirect
SECURE_SSL_REDIRECT = True
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# Force HTTPS in the final URIs
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

AWS_STORAGE_BUCKET_NAME = 'elasticbeanstalk-us-east-2-301906610566'
AWS_S3_REGION_NAME = 'us-east-2'  # e.g. us-east-2
AWS_ACCESS_KEY_ID = 'AKIAJHDEF6QMN2NUI4IA'
with open('aws_secret_key.txt') as f:
	AWS_SECRET_ACCESS_KEY = f.read().strip()

# Tell django-storages the domain to use to refer to static files.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# Tell the staticfiles app to use S3Boto3 storage when writing the collected static files (when
# you run `collectstatic`).
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'custom_storages.StaticStorage'
MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
