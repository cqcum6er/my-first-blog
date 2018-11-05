"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2)z6gao=dn=csifbos_a&8sr5h6#%%imru@l=y*elf)e+c*3ta'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False  #Check "User comment" error before turning off.

ALLOWED_HOSTS = []  #Set to ['127.0.0.1', 'cqcum6er.pythonanywhere.com', 'www.fundamentaltrader.net'] when DEBUG is set to False, otherwise leave empty.


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'blog',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,  #Django will search all of your apps for a folder named \templates.
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  #Allows use of 'request' in templates.
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),  #Can also use '/home/<my name>/<my_test_project>/db.sqlite3' when moving project to pythonanywhere
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

#Enable email capability below.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  #Use 'django.core.mail.backends.console.EmailBackend' for local test.
EMAIL_HOST = 'smtp.gmail.com'  #"pop.mail.yahoo.com" use "smtp.mail.yahoo.com" when receiving in yahoo; use "localhost" when doing local test.
EMAIL_PORT = 465 #587 995  #use 1025 when doing local test.
DEFAULT_FROM_EMAIL = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
#EMAIL_USE_TLS = True
EMAIL_USE_SSL = True
