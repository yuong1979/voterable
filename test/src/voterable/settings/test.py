"""
Django settings for voterable project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# confidential
SECRET_KEY = '1$9!@pw#%of5sf)u$*yiv)q)(q+8-xxg4yu_&ri%fvfdp06bk#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
















TYPE = "testing"

EMAIL_BACKEND = 'django_ses.SESBackend'
DEFAULT_FROM_EMAIL = 'hello@voterable.com'
# These are optional -- if they're set as environment variables they won't
# need to be set here as well
AWS_SES_ACCESS_KEY_ID = 'AKIAJZN7CKPA3GURQOTA'
AWS_SES_SECRET_ACCESS_KEY = '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'

# Additionally, if you are not using the default AWS region of us-east-1,
# you need to specify a region, like so:
AWS_SES_REGION_NAME = 'us-west-2'
AWS_SES_REGION_ENDPOINT = 'email.us-west-2.amazonaws.com'

STRIPE_PUBLISHABLE = os.getenv('STRIPE_PUBLISHABLE','pk_test_gYemm4pYUHZufj7WAlFE5owC')
STRIPE_SECRET = os.getenv('STRIPE_SECRET','sk_test_ghdJXX8eWjTYglGMNFO4woVZ')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

#necessary for django captcha
    'captcha',

#necessary for django allauth
    'django.contrib.sites',
#necessary for django ses
    'django_ses',
    'pagedown',

#installed apps
    'crispy_forms',
    'django_cleanup',
    'polls',
    'users',
    'mixins',

    'home',
    'messaging',
    'tags',
    'variable',
    'analytics',
    'billing',
    'notifications',
    'micell',

#necessary for django allauth

    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.instagram',
    
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # simple wysiwyg editor:
    'django_summernote',

    # firebase
    'firebasenotifications',
    # 'fcm',

    'rest_framework',

]


# simple wysiwyg editor settings :
SUMMERNOTE_CONFIG = {
    # all options here: https://github.com/summernote/django-summernote#options
    # Change editor size
    'width': '100%',
    'height': '300',
    'iframe': False,
    'toolbar': [
        # [groupName, [list of button]] help: https://summernote.org/deep-dive/#custom-toolbar-popover
        ['style', ['style']],
        ['font', ['bold', 'italic', 'underline']],
        ['para', ['ul', 'ol', 'paragraph']],
        ['height', ['height']],
        ['insert', ['link', 'picture', 'videoAttributes']],
        ['view', ['fullscreen']],
    ],
}


#necessary for django allauth - this will call the id of the site we are using to be attached
#to the emails we send out - eg th default is example.com
SITE_ID = 2

#necessary for django allauth
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)


# necessary for django allauth
# ACCOUNT_AUTHENTICATION_METHOD ="username" | "email" | "username_email"
ACCOUNT_AUTHENTICATION_METHOD ="username_email"
ACCOUNT_EMAIL_REQUIRED=True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS =1
ACCOUNT_EMAIL_VERIFICATION ="mandatory"
ACCOUNT_UNIQUE_EMAIL =True
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION =True
ACCOUNT_SIGNUP_FORM_CLASS = 'home.forms.AllauthSignupForm'
LOGIN_REDIRECT_URL='/'
SOCIALACCOUNT_EMAIL_VERIFICATION="none"

ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"

# reCAPTCHA settings
RECAPTCHA_PUBLIC_KEY = '6LdZ7TUUAAAAAPaU9UfYTaJlTrM7Mtf1NjOtJvYg'
RECAPTCHA_PRIVATE_KEY = '6LdZ7TUUAAAAAB2FFWG9NUZ-HIKYQHKxuZbTug6-'
NOCAPTCHA = True
RECAPTCHA_USE_SSL = False


CRISPY_TEMPLATE_PACK = 'bootstrap3'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'voterable.urls'

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
            'libraries': {
                'poll_extras': 'polls.templatetags.poll_extras',

            }
        },
    },
]

WSGI_APPLICATION = 'voterable.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# confidential
# localhost - need to install postgres under pip install and start a new database in the 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db',
        'USER': 'admin',
        'PASSWORD': '1234qwer',
        'HOST': 'ip-172-31-11-167.ap-southeast-1.compute.internal',
        'PORT': '5432',
    }
}
# ip-172-31-11-167.ap-southeast-1.compute.internal
# ec2-13-229-65-97.ap-southeast-1.compute.amazonaws.com

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

TIME_ZONE = 'Asia/Singapore'

USE_I18N = True

USE_L10N = True

USE_TZ = True







AWS_STORAGE_BUCKET_NAME = 'voterable-test-bucket'
AWS_ACCESS_KEY_ID = 'AKIAJWOKTEYROCOQPBWA'
AWS_SECRET_ACCESS_KEY = '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'

# Tell django-storages that when coming up with the URL for an item in S3 storage, keep
# it simple - just use this domain plus the path. (If this isn't set, things get complicated).
# This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it.
# We also use it in the next setting.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

STATICFILES_LOCATION = 'static'
MEDIAFILES_LOCATION = 'media'
# This is used by the `static` template tag from `static`, if you're using that. Or if anything else
# refers directly to STATIC_URL. So it's safest to always set it.
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
# Tell the staticfiles app to use S3Boto storage when writing the collected static files (when
# you run `collectstatic`).
STATICFILES_STORAGE = 'custom_storages.StaticStorage'
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'



# https://developers.facebook.com/apps/763309543823457/fb-login/settings/

# http://localhost:8000/

# http://localhost:8000/accounts/facebook/login/callback
# http://127.0.0.1:8000/accounts/facebook/login/callback
# http://www.teach-advisor.com/accounts/facebook/login/callback
# https://www.teach-advisor.com/accounts/facebook/login/callback
# http://teach-advisor.com/accounts/facebook/login/callback
# https://teach-advisor.com/accounts/facebook/login/callback

# https://console.developers.google.com/projectselector/apis/library

# http://127.0.0.1:8000/accounts/google/login/callback/
# http://localhost:8000/accounts/google/login/callback/

# http://www.teach-advisor.com/accounts/google/login/callback
# https://www.teach-advisor.com/accounts/google/login/callback
# http://teach-advisor.com/accounts/google/login/callback
# https://teach-advisor.com/accounts/google/login/callback

# http://teach-advisor.com/
# https://teach-advisor.com/




SOCIALACCOUNT_PROVIDERS = \
    {'facebook':
       {'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile', 'user_friends'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time'],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': lambda request: 'en_US}',
        'VERIFIED_EMAIL': True,
        'VERSION': 'v2.4'}}

SOCIALACCOUNT_PROVIDERS = \
    { 'google':
        { 'SCOPE': ['profile', 'email'],
          'AUTH_PARAMS': { 'access_type': 'online' } }}


### BLEACH
BLEACH_ALLOWED_ATTRIBUTES = {
    'iframe': ['width', 'height', 'src', 'frameborder', 'class'],
    'img': ['style', 'src', 'class'],
    'a': ['href']
}

BLEACH_ALLOWED_STYLES = ['width', 'height']
### END BLEACH




# # Firebase Related Settings

# Server Key found under project settings -> cloud messaging
# SERVER_KEY = 'AAAAZp1PDlM:APA91bGvEYakMq956I2iHA8wsHN9E9L3GO6S-AuWvs520cX-R7qminSiv' \
#              'PBGvjejCVgoe4waDappEVV2eCLOzQSGlQaFgF5iGzz4X0uf8-CNSEudEcjDDCpiJTyEh_oEKOWCVc_9wc4J'

SERVER_KEY = 'AAAAeQG8tYI:APA91bGvvs29a2MgSu8PCcuk3VXXNMUGaJT1sxCUqK576C5Gkqx-ZKNbQ2R' \
             'rSgR-cWplJ9Vg75mInoOxxzy32ng6Q_2YCw0ibOOE_WEwrh-s8n-u-1L87sdd67K_ZVFL1A7gU_32YxrA'


# # apiKey
# API_KEY = 'AIzaSyANxM3W8UaFMNYixRe15NY61p4WNoEBqog'

# new apiKey
API_KEY = 'AIzaSyCrt7-QOYmxzNDZoJqJhorIWJBytBoLoPc'

# # messagingSenderId
# SENDER_ID = 440725868115

# new messagingSenderId
SENDER_ID = 519720187266

# topic name
TOPIC_NAME = 'voterable'

MESSAGE_BODY='Checkout new and exciting updates at voterable!'

MESSAGE_TITLE = 'Hello User'

CLICK_ACTION = 'https://www.voterable.com/notifications/'

NOTIFICATION_ICON = 'https://s3-ap-southeast-1.amazonaws.com/voterable-prod-bucket/static/img/voterable+logo.JPG'





#using redis
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE










# #using aws sqs
# AWS_ACCESS_KEY_ID='AKIAIHIMTXXYUBBENRVA'
# AWS_SECRET_ACCESS_KEY='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'

# CELERY_BROKER_URL = 'sqs://%s:%s@' % (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
# CELERY_BROKER_TRANSPORT = 'sqs'
# # CELERY_BROKER_TRANSPORT_OPTIONS = {
# #     'region': 'ap-southeast-1',
# # }
# CELERY_BROKER_USER = AWS_ACCESS_KEY_ID
# CELERY_BROKER_PASSWORD = AWS_SECRET_ACCESS_KEY
# CELERY_WORKER_STATE_DB = '/var/run/celery/worker.db'
# CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
# CELERY_WORKER_PREFETCH_MULTIPLIER = 0
# BROKER_TRANSPORT_OPTIONS = {
#     'region': 'ap-southeast-1',
#     'polling_interval': 3,
#     'visibility_timeout': 3600,
# }


# # CELERY_BROKER_URL = 'redis://localhost:6379'
# # CELERY_RESULT_BACKEND = 'redis://localhost:6379'
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = TIME_ZONE

# CELERY_DEFAULT_QUEUE = 'celery'
# CELERY_QUEUES = {
#     CELERY_DEFAULT_QUEUE: {
#         'exchange': CELERY_DEFAULT_QUEUE,
#         'binding_key': CELERY_DEFAULT_QUEUE,
#     }
# }
