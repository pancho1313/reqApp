"""
Django settings for reqAdmin project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wr!5dlcbavy@#xn61+i*!6z$#%uuh75i3seo)6e%bxaxpkx6z*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'reqApp',
    'tinymce',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'reqAdmin.urls'

WSGI_APPLICATION = 'reqAdmin.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mainReqDB',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Chile/Continental'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# login/logout
LOGIN_URL = 'reqApp:login'
LOGIN_REDIRECT_URL = 'reqApp:PR' # selectProject.html
LOGOUT_URL = 'reqApp:login'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages'
)

# Tiny-mce
TINYMCE_JS_URL = os.path.join(STATIC_URL, "js/tiny_mce/tiny_mce.js")
TINYMCE_JS_ROOT = os.path.join(STATIC_URL, "tiny_mce/")

# doc. img. upload folder
IMAGES_UPLOAD = 'uploads/'

# email
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com' # larga vida a google
EMAIL_PORT = 587
EMAIL_HOST_USER = 'mainreq.90@gmail.com' # inserte su gmail
EMAIL_HOST_PASSWORD = 'NataliaPoklonskaia' # y su contrasegnia
