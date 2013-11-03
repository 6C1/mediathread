# flake8: noqa
from mediathread.settings import *

#TEMPLATE_DIRS = (
#    "/var/www/mediathread/mediathread/mediathread/deploy_specific/templates",
#    "/var/www/mediathread/mediathread/mediathread/templates",
#)

MEDIA_ROOT = '/var/www/vhosts/klein/mediathread/uploads/'
# put any static media here to override app served static media
STATICMEDIA_MOUNTS = (
    ('/sitemedia', '/var/www/vhosts/klein/sitemedia'),
)

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'mediathread',
#        'HOST': '',
#        'PORT': 6432,  # see /etc/pgbouncer/pgbouncer.ini
#        'USER': '',
#        'PASSWORD': '',
#    }
#}

COMPRESS_ROOT = "/var/www/vhosts/klein/media/"
DEBUG = True
TEMPLATE_DEBUG = DEBUG

#SENTRY_SITE = 'mediathread'
#SENTRY_SERVERS = ['http://sentry.ccnmtl.columbia.edu/sentry/store/']

if 'migrate' not in sys.argv:
    INSTALLED_APPS.append('raven.contrib.django')

    import logging
    from raven.contrib.django.handlers import SentryHandler
    logger = logging.getLogger()
    # ensure we havent already registered the handler
    if SentryHandler not in map(type, logger.handlers):
        logger.addHandler(SentryHandler())
        logger = logging.getLogger('sentry.errors')
        logger.propagate = False
        logger.addHandler(logging.StreamHandler())

FLOWPLAYER_SWF_LOCATION='http://klein.dartmouth.edu/site_media/flowplayer/flowplayer-3.2.16.swf'
FLOWPLAYER_AUDIO_PLUGIN = 'flowplayer.audio-3.2.10.swf'
FLOWPLAYER_PSEUDOSTREAMING_PLUGIN = 'flowplayer.pseudostreaming-3.2.12.swf'
FLOWPLAYER_RTMP_PLUGIN = 'flowplayer.rtmp-3.2.12.swf'

try:
    from local_settings import *
except ImportError:
    pass
