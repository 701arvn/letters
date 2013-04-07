# encoding: utf-8
# Django settings for letterpress project.
import os
import random
import dj_database_url
from mongoengine import connect

DEBUG = os.environ.get('DJANGO_DEBUG', '0') == '1'
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['.herokuapp.com']

ADMINS = (
    ('Evgeny Tataurov', 'tatauroff@gmail.com'),
)

MANAGERS = ADMINS

MONGO_DATABASE_NAME = 'letters'  # This isn't used on Heroku
MONGO_HOST = os.environ.get('MONGOHQ_URL', 'localhost')
MONGO_PORT = 27017
connect(MONGO_DATABASE_NAME, host=MONGO_HOST, port=MONGO_PORT)

DATABASES = {
    # Parse database configuration from $DATABASE_URL
    'default': dj_database_url.config(),
}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

PROJECT_DIR = os.path.join(os.path.dirname(__file__), os.pardir)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_DIR, 'staticfiles')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'letterpress.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'letterpress.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'lpmessage',
    'lpgame',
    'mongonaut',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'social_auth',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '[%(asctime)s - %(module)s] %(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'lpgame': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
}

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'django.contrib.auth.backends.ModelBackend',
)
# Если имя не удалось получить, то можно его сгенерировать
SOCIAL_AUTH_DEFAULT_USERNAME = lambda: random.choice(['Darth_Vader', 'Obi-Wan_Kenobi', 'R2-D2', 'C-3PO', 'Yoda'])
# Разрешаем создавать пользователей через social_auth
SOCIAL_AUTH_CREATE_USERS = True

# Перечислим pipeline, которые последовательно буду обрабатывать респонс 
SOCIAL_AUTH_PIPELINE = (
    # Получает по backend и uid инстансы social_user и user
    'social_auth.backends.pipeline.social.social_auth_user',
    # Получает по user.email инстанс пользователя и заменяет собой тот, который получили выше.
    # Кстати, email выдает только Facebook и GitHub, а Vkontakte и Twitter не выдают
    'social_auth.backends.pipeline.associate.associate_by_email',
    # Пытается собрать правильный username, на основе уже имеющихся данных
    'social_auth.backends.pipeline.user.get_username',
    # Создает нового пользователя, если такого еще нет
    'social_auth.backends.pipeline.user.create_user',
    # Пытается связать аккаунты
    'social_auth.backends.pipeline.social.associate_user',
    # Получает и обновляет social_user.extra_data
    'social_auth.backends.pipeline.social.load_extra_data',
    # Обновляет инстанс user дополнительными данными с бекенда
    'social_auth.backends.pipeline.user.update_user_details'
)

LOGIN_REDIRECT_URL = '/'

LOGIN_URL = '/login/'

# These should be overwritten in local_settings or in config vars
SECRET_KEY = os.environ.get('SECRET_KEY', '')

ASYNC_BACKEND_URL = os.environ.get('ASYNC_BACKEND_URL', '')

TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY', '')
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET', '')


try:
    from local_settings import *
except ImportError:
    pass
