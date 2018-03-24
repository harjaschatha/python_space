"""
Django settings for stephens project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_f6w7c)tdm)=%cidz6)2kmi7+k=+6o65$d5zi9eiz_$l($blsl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []

SITE_ID=1


# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    'office',
    'mainsite',
    'attendance',
    'admission',
    'college_forms',
    'events',
    'captcha',
    #'archive',
    #'django.contrib.flatpages',
    
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',   
)

ROOT_URLCONF = 'stephens.urls'

WSGI_APPLICATION = 'stephens.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = None

USE_I18N = False

USE_L10N = False

USE_TZ = False

USE_ETAGS=True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
MEDIA_URL='/media/'
STATIC_URL = '/static/'
#===================================================================
MEDIA_ROOT=os.path.join(BASE_DIR,'mediafiles')
STATIC_ROOT=os.path.join(BASE_DIR,'staticfiles')
#===================================================================


LOGIN_REDIRECT_URL='/profile/'
LOGIN_URL='/login'
TEMPLATE_DIRS=[os.path.join(BASE_DIR,'templates')]
#the domain name to be associated with the file viewers
domain_name='http://localhost:8000'



EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "web.dev.ssc@gmail.com"
EMAIL_HOST_PASSWORD = 'arjoonnsharma'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

