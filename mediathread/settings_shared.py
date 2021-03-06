# Django settings for mediathread project.

# if you add a 'deploy_specific' directory
# then you can put a settings.py file and templates/ overrides there
# (see bottom)

from courseaffils import policies
import os.path
import re
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = (
    ('john', 'john@novomancy.org'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = ['.dartmouth.edu', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mediathread',
        'HOST': 'localhost',
        'PORT': '5432',
        'USER': 'mthread',
        'PASSWORD': 'jZKqt4bUUn',
    }
}

if 'test' in sys.argv or 'jenkins' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
            'HOST': '',
            'PORT': '',
            'USER': '',
            'PASSWORD': '',
        }
    }

JENKINS_TASKS = (
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.django_tests',
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
)

PROJECT_APPS = ['mediathread.main',
                'mediathread.djangosherd',
                'mediathread.assetmgr',
                'mediathread.projects',
                'mediathread.reports',
                'mediathread.discussions']

#TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
#NOSE_ARGS = [
#    '--with-coverage',
#    ('--cover-package=mediathread.main,mediathread.djangosherd,'
#     'mediathread.assetmgr,mediathread.projects'),
#]

CACHE_BACKEND = 'locmem:///'

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
MEDIA_ROOT = "uploads/"
MEDIA_URL = '/uploads/'
STATIC_URL = '/media/'

#appends a slash if nothing is found without a slash.
APPEND_SLASH = True

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)

# ## be careful: if you add/remove something here
# ## do the same with settings_production.py
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'mediathread.main.views.django_settings',
    'stagingcontext.staging_processor',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'courseaffils.middleware.CourseManagerMiddleware',
    'mediathread.main.middleware.AuthRequirementMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
)

ROOT_URLCONF = 'mediathread.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates"
    # or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # Put application templates before these fallback ones:
    "/var/www/vhosts/klein/mediathread/templates/",
    os.path.join(os.path.dirname(__file__), "deploy_specific/templates"),
    os.path.join(os.path.dirname(__file__), "templates"),
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.flatpages',
    'django.contrib.markup',
    'sorl.thumbnail',
    'courseaffils',
    'django.contrib.sites',
    'django.contrib.admin',
    'tagging',
    'smartif',
    'modelversions',
    'structuredcollaboration',
    'mediathread.djangosherd',
    'mediathread.assetmgr',
    'mediathread.projects',
    'mediathread.discussions',
    'django.contrib.comments',
    'threadedcomments',
    'djangohelpers',
    'mediathread.reports',
    'mediathread.main',
    'south',
#    'django_nose',
    'compressor',
    'django_jenkins',
    'mediathread.taxonomy',
    'smoketest'
]

COMPRESS_URL = "/site_media/"
COMPRESS_ROOT = "media/"
COMPRESS_PARSER = "compressor.parser.HtmlParser"

THUMBNAIL_SUBDIR = "thumbs"
EMAIL_SUBJECT_PREFIX = "[mediathread] "
EMAIL_HOST = 'localhost'
SERVER_EMAIL = "john@novomancy.org"
PUBLIC_CONTACT_EMAIL = "john@novomancy.org"

# External url for issue reporting system or e-mail notification
CONTACT_US_DESTINATION = ""

DATE_FORMAT = DATETIME_FORMAT = "g:i a, m/d/y"
LOGOUT_REDIRECT_URL = LOGIN_REDIRECT_URL = '/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


# for AuthRequirementMiddleware. this should be a list of
# url prefixes for paths that can be accessed by anonymous
# users. we need to allow anonymous access to the login
# page, and to static resources.

ANONYMOUS_PATHS = ('/site_media/',
                   '/accounts/',
                   '/admin/',
                   '/api/',
                   '/help/'
                   )

NON_ANONYMOUS_PATHS = ('/asset/',
                       '/annotations/',
                       '/contact/',
                       '/yourspace/',
                       '/project/',
                       '/explore/',
                       '/comments/',
                       '/reports/',
                       '/discussion/',
                       '/archive/',
                       '/assignment/',
                       '/dashboard/',
                       '/_main/',
                       '/analysis/',
                       '/taxonomy/',
                       re.compile(r'^/$'),
                       )

# save is an exception, for server2server api
COURSEAFFILS_PATHS = NON_ANONYMOUS_PATHS + ('/save', '/settings')

COURSEAFFILS_EXEMPT_PATHS = ANONYMOUS_PATHS
COURSEAFFIL_AUTO_MAP_GROUPS = ['demo']

COMMENTS_ALLOW_PROFANITIES = True
COMMENTS_APP = 'threadedcomments'
COMMENT_MAX_LENGTH = None

FORCE_LOWERCASE_TAGS = True

# if you set this to a string, then bookmarklet can import from flickr
DJANGOSHERD_FLICKR_APIKEY = None

# Mediathread instantiates a Flowplayer .swf to play many video flavors.
# Update this variable with your site's Flowplayer installation
# See README.markdown for more information
# expected: http://<server>/<directory>/flowplayer-3.2.15.swf
#FLOWPLAYER_SWF_LOCATION = None
# Specify your own plugin versions here. The player looks in the same
# http://<server>/<directory>/ specified above.
#FLOWPLAYER_AUDIO_PLUGIN = 'flowplayer.audio-3.2.10.swf'
#FLOWPLAYER_PSEUDOSTREAMING_PLUGIN = 'flowplayer.pseudostreaming-3.2.11.swf'
#FLOWPLAYER_RTMP_PLUGIN = 'flowplayer.rtmp-3.2.11.swf'


FLOWPLAYER_SWF_LOCATION='http://klein.dartmouth.edu/site_media/flowplayer/flowplayer-3.2.16.swf'
FLOWPLAYER_AUDIO_PLUGIN = 'flowplayer.audio-3.2.10.swf'
FLOWPLAYER_PSEUDOSTREAMING_PLUGIN = 'flowplayer.pseudostreaming-3.2.12.swf'
FLOWPLAYER_RTMP_PLUGIN = 'flowplayer.rtmp-3.2.12.swf'

DEFAULT_COLLABORATION_POLICY = policies.InstructorManaged()


# this gets around Django 1.2's stupidity for commenting
# we're already checking that the request is from someone in the class
def no_reject(request, reason):
    request.csrf_processing_done = True
    return None

CSRF_FAILURE_VIEW = no_reject

# if you add a 'deploy_specific' directory
# then you can put a settings.py file and templates/ overrides there
try:
    from mediathread.deploy_specific.settings import *
    if 'EXTRA_INSTALLED_APPS' in locals():
        INSTALLED_APPS = INSTALLED_APPS + EXTRA_INSTALLED_APPS
    if 'EXTRA_MIDDLEWARE_CLASSES' in locals():
        MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + EXTRA_MIDDLEWARE_CLASSES
except ImportError:
    pass
