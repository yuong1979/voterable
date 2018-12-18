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
SECRET_KEY = '^4cuuul=3%a7w$f_fmo*l3t-9q_%hfy%fs5-)u!75m%@z_4j29'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
















TYPE = "base"

# using gmail
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "Balancedtechsgp@gmail.com"
EMAIL_MAIN = "Balancedtechsgp"
EMAIL_HOST_PASSWORD = "fakeready24"
EMAIL_PORT = 587
EMAIL_USE_TLS = True





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
    'popover': {
        'air': [
            # ['insert', ['link', 'picture', 'video']]
            ['insert', ['link', 'picture', 'videoAttributes']],
        ]
    }
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



# reCAPTCHA settings
RECAPTCHA_PUBLIC_KEY = '6LeX7TUUAAAAAGwTZFZ1bt2d3riVENfVs8Yx_-1C'
RECAPTCHA_PRIVATE_KEY = '6LeX7TUUAAAAAItwRNvyQ_m0KKKH_L_NoyOpOxBp'
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}




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







# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

# start a folder such as the below(staticinpro/ourstatic) and dump all the static/image 
# files inside and after running the collect static the system will dump all 
# staticinpro/ourstatic files into the static_in_env/static_root and media_root
# after loading the files into staticinpro folder you dont need to run collectstatic
# but you need to use {% load staticfiles %} and "{% static 'img/marketing1.jpg' %}"
# to load the files
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(BASE_DIR), "static_in_pro", "our_static"),
    #os.path.join(BASE_DIR, "static_in_env"),
    #'/var/www/static/',
)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_in_env", "static_root")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_in_env", "media_root")

# Protected has no url
PROTECTED_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_in_env", "protected_root")
# print BASE_DIR


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






CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE





# import djcelery
# djcelery.setup_loader()
# import datetime

# CELERYBEAT_SCHEDULE = {
#     'add-every-60-seconds': {
#         'task': 'home.tasks.periodic_func',
#         'schedule': datetime.timedelta(seconds=60)
#     },
# }

# CELERY_TIMEZONE = 'UTC'
# # https://sqs.ap-southeast-1.amazonaws.com/115264615317/testqueue
# BROKER_URL = 'https://sqs.ap-southeast-1.amazonaws.com/115264615317/testqueue'
# BACKEND_URL = 'https://sqs.ap-southeast-1.amazonaws.com/115264615317/testqueue'


# AWS_ACCESS_KEY_ID = 'AKIAISBDYLWMWDE344EQ'
# AWS_SECRET_ACCESS_KEY = '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'


# # BROKER_URL = 'sqs://AKIAISBDYLWMWDE344EQ:PKrFS/4cVrr097Qdrnxmfib0QnhYQo5/Fo/u7LxF@'
# # BACKEND_URL = 'sqs://AKIAISBDYLWMWDE344EQ:PKrFS/4cVrr097Qdrnxmfib0QnhYQo5/Fo/u7LxF@'


# # BROKER_URL = 'sqs://{0}:{1}@'.format(
# #     urllib.parse.quote(AWS_ACCESS_KEY_ID, safe=''),
# #     urllib.parse.quote(AWS_SECRET_ACCESS_KEY, safe='')
# # )

# # BACKEND_URL = 'sqs://{0}:{1}@'.format(
# #     urllib.parse.quote(AWS_ACCESS_KEY_ID, safe=''),
# #     urllib.parse.quote(AWS_SECRET_ACCESS_KEY, safe='')
# # )



# BROKER_TRANSPORT_OPTIONS = {
#     'region': 'ap-southeast-1',
#     'polling_interval': 3,
#     'visibility_timeout': 3600,
# }
# BROKER_TRANSPORT_OPTIONS['queue_name_prefix'] = 'repricer-stage-'
# CELERY_SEND_TASK_ERROR_EMAILS = True



# # Firebase Related Settings

# Server Key found under project settings -> cloud messaging
SERVER_KEY = 'AAAAwzumhNY:APA91bGN8Gwj7-vwre05XzZcrQFXBDxd-NIOQjlpE_kcfPOSP_o0k2ECxzgQH0' \
             'fh_LJhWDlz9H4ROTlho40H4Qf39xX3FQ42FOjQM0PrINq_30ewgIHTDkdeKhh3OCdMMIi_5HsQC4UH'


# apiKey
API_KEY = 'AIzaSyCvd2Dw2i7rtNDByl6mmplyPebHMUy9bis'

# messagingSenderId
SENDER_ID = 838519391446

# topic name
TOPIC_NAME = 'voterable'

MESSAGE_BODY='Checkout new and exciting updates at voterable!'

MESSAGE_TITLE = 'Hello User'

CLICK_ACTION = 'http://localhost:8000/tags/'