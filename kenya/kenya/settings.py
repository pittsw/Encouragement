# Django settings for kenya project.

# Necessary for updating
from datetime import timedelta
URGENT = timedelta(days=14)

# Necessary for SMSSync view.
TRANSPORT = 'shujaa'
SMSSYNC_SECRET = 'Standards'

# Default Settings For System.
DEFAULT_NURSE_NAME = "Dyphna"

# These settings must be set to use Celery
import djcelery
djcelery.setup_loader()
BROKER_URL = "amqp://guest:guest@localhost:5672/"
#BROKER_PORT = 5672
#BROKER_USER = "guest"
#BROKER_PASSWORD = "guest"
#BROKER_VHOST = "/"
CELERY_IMPORTS = ('patients.tasks')

DEBUG = True
TEMPLATE_DEBUG = DEBUG

AUTH_PROFILE_MODULE = 'patients.Nurse'

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

import os
ROOT_PATH = os.path.dirname(__file__)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'encouragement',
        'USER': 'kenya',
        'PASSWORD': 'kenya'
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Africa/Dar_es_Salaam'

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
MEDIA_ROOT = str(ROOT_PATH) + '/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = str(ROOT_PATH) + '/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'q&amp;+l4olv@z4^o5hdi!v-zw!xrww%st0pol9k=b^)nr_+5amw_+'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
	 'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
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

ROOT_URLCONF = 'kenya.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'kenya.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'patients',
    'httpsms',
    'transport_email',
    #'smssync',
    'backend',
    'djcelery',
    'south',
)

# choose a path that is your virtual environment root
VENV_ROOT = os.path.join('/','tmp/','encouragement')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
            'datefmt' : '%Y-%m-%d %H:%M:%S'
        },
        'message': {
            'format': '%(asctime)s,%(message)s',
            'datefmt' : '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'transport_message_log': {                # define and name a handler
            'level': 'DEBUG',
            'class': 'logging.FileHandler', # set the logging class to log to a file
            'formatter': 'message',         # define the formatter to associate
            'filename': os.path.join(VENV_ROOT, 'messages.log') # log file
        },

        'encouragement_log': {                 # define and name a second handler
            'level': 'DEBUG',
            'class': 'logging.FileHandler', # set the logging class to log to a file
            'formatter': 'verbose',         # define the formatter to associate
            'filename': os.path.join(VENV_ROOT, 'encouragement.log')  # log file
        },
    },
    'loggers': {
        'logview.transport': {              # define a logger - give it a name
            'handlers': ['transport_message_log'], # specify what handler to associate
            'level': 'INFO',                 # specify the logging level
            'propagate': True,
        },     

        'logview.encouragement': {               # define another logger
            'handlers': ['encouragement_log'],  # associate a different handler
            'level': 'INFO',                 # specify the logging level
            'propagate': True,
        },        
    }       
}

#Import local settings
from settings_local import *

if 'LOCAL_LOGGING' in globals():
	#overwrite with local logging settings
	import collections
	
	def merge(old,new):
		for k,v in new.iteritems():
			if isinstance(v,collections.Mapping):
				r = merge(old.get(k,{}),v)
				old[k] = r
			else:
				old[k] = new[k]
		return old
		
	LOGGING = merge(LOGGING,LOCAL_LOGGING)
