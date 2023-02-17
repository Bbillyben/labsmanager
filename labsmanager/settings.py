"""
Django settings for labsmanager project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from django.conf.locale.es import formats as es_formats  # to set dateformat over the app
import os
from .config import get_setting, get_boolean_setting
import logging

logger = logging.getLogger('labsmanager')



es_formats.DATETIME_FORMAT = "d M Y H:i:s"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_setting('SECRET_KEY', 'secret_key', 'django-insecure,klsdh0989è_çà$*ùùjkoijç_015.BHh_dq')  
# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = get_boolean_setting("DEBUG", "debug", default_value=False)  

# Configure logging settings
log_level = get_setting('LABS_LOG_LEVEL', 'log_level', 'WARNING')

logging.basicConfig(
    level=log_level,
    format="%(asctime)s %(levelname)s %(message)s",
)

if log_level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
    log_level = 'WARNING'  # pragma: no cover

logger.debug("-------------------------- Start debug session  --------------------------")

ALLOWED_HOSTS =  get_setting('DJANGO_ALLOWED_HOSTS', 'django_allowed_hosts', '*').split(" ") # ['*']  os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")


# Application definition

INSTALLED_APPS = [
    # Django Base
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_q',

    # Installed Package
    'crispy_forms',                 # https://django-crispy-forms.readthedocs.io/en/latest/install.html
    'view_breadcrumbs',             # https://pypi.org/project/django-view-breadcrumbs/#add-view_breadcrumbs-to-your-installed_apps
    'django_tables2',               # https://django-tables2.readthedocs.io/en/latest/
    'rest_framework',               # https://www.django-rest-framework.org/
    'rest_framework.authtoken',
    'bootstrap_modal_forms',        # https://pypi.org/project/django-bootstrap-modal-forms/
    'mptt',                         # https://django-mptt.readthedocs.io/en/latest/tutorial.html
    'django_pivot',                 # https://github.com/martsberger/django-pivot
    'auditlog',                     # https://django-auditlog.readthedocs.io/en/latest/installation.html
    #                                 # https://django-easy-pdf.readthedocs.io/en/v0.2.0-dev1/installation.html
    'dbbackup',                     # https://django-dbbackup.readthedocs.io/en/master/installation.html
    'tabular_permissions',          # https://pypi.org/project/django-tabular-permissions/
    'import_export',                # https://django-import-export.readthedocs.io/en/latest/installation.html
    'django_filters',               # https://django-filter.readthedocs.io/en/stable/guide/install.html
    'colorfield',                   # to get a color field
    'django_js_reverse',            # get reverse url in javascript file https://github.com/ierror/django-js-reverse
    'faicon',                        #https://pypi.org/project/django-faicon/
    
    # App
    'staff.apps.StaffConfig',
    'project.apps.ProjectConfig',
    'fund.apps.FundConfig',
    'expense.apps.ExpenseConfig',
    'settings.apps.SettingsConfig',
    'endpoints.apps.EndpointsConfig',
    'leave.apps.LeaveConfig',
    'common.apps.CommonConfig',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'auditlog.middleware.AuditlogMiddleware',
]

ROOT_URLCONF = 'labsmanager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries':{
                'customs_tags': 'labsmanager.templatetags.customs_tags',
            
            }
        },
    },
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

WSGI_APPLICATION = 'labsmanager.wsgi.application'




DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'data' / 'dbs' / 'db.sqlite3',
    # },
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_setting('LAB_DB_NAME', 'lab_db_name', 'labsmanager'),
        'USER': get_setting('LAB_DB_USER', 'lab_db_user', 'labsmanager'), 
        'PASSWORD': get_setting('LAB_DB_PASSWORD', 'lab_db_password', 'labsManagerPass'),
        'HOST': get_setting('LAB_DB_HOST', 'lab_db_host', 'localhost'), 
        'PORT': get_setting('LAB_DB_PORT', 'lab_db_port', '5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

if get_setting('CSRF_TRUSTED_ORIGINS', 'csrf_trusted_origins', False):
    CSRF_TRUSTED_ORIGINS =  get_setting('CSRF_TRUSTED_ORIGINS', 'csrf_trusted_origins', False).split()
else:
    CSRF_TRUSTED_ORIGINS=[]

logger.debug('CSRF_TRUSTED_ORIGINS :'+str(CSRF_TRUSTED_ORIGINS))   

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_TZ = True

LANGUAGES = [
    ('en','English'),
    ('fr', 'Français')
]


# Static files (CSS, JavaScript, Images)

STATIC_ROOT = '/home/labsmanager/data/static/'

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "data" / "static",
]

# Color Themes Directory
STATIC_COLOR_THEMES_DIR = os.path.join(STATIC_URL, 'css', 'color-themes')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# crispy forms use the bootstrap templates
CRISPY_TEMPLATE_PACK = 'bootstrap4'

SITE_ID=get_setting('LAB_SITE_ID', 'site_id', 1, int)
logger.debug('SITE_ID :'+str(SITE_ID))


LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/" 

# rest framework
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
       
   ),
}

APPEND_SLASH = False  # prevent error for post request by ajax

# for django Q
# Configure your Q cluster
# More details https://django-q.readthedocs.io/en/latest/configure.html
Q_CLUSTER = {
    'retry': 60,
    'timeout': 30,
    'workers': 4,
    "name": "labsmanager",
    "orm": "default",  # Use Django's ORM + database for broker
    'save_limit': 250,
    'label': 'Scheduled Tasks',
}


# Session 
SESSION_COOKIE_AGE = 6400


## Import export options

IMPORT_EXPORT_USE_TRANSACTIONS = True

## aduit log
AUDITLOG_DISABLE_ON_RAW_SAVE = True

## breadcrumbs
BREADCRUMBS_HOME_LABEL = '<i class="fas fa-bars"></i>'


## EMAIL
EMAIL_BACKEND = get_setting('LAB_EMAIL_BACKEND', 'email.backend', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = get_setting('LAB_EMAIL_HOST', 'email.host', '')
EMAIL_PORT = get_setting('LAB_EMAIL_PORT', 'email.port', 25, typecast=int)
EMAIL_HOST_USER = get_setting('LAB_EMAIL_USERNAME', 'email.username', '')
EMAIL_SENDER = get_setting('LAB_EMAIL_SENDER', 'email.sender', '')
EMAIL_HOST_PASSWORD = get_setting('LAB_EMAIL_PASSWORD', 'email.password', '')
EMAIL_SUBJECT_PREFIX = get_setting('LAB_EMAIL_PREFIX', 'email.prefix', '[InvenTree] ')
EMAIL_USE_TLS = get_boolean_setting('LAB_EMAIL_TLS', 'email.tls', False)
EMAIL_USE_SSL = get_boolean_setting('LAB_EMAIL_SSL', 'email.ssl', False)

DEFAULT_FROM_EMAIL = EMAIL_SENDER


## Admins
ADMINS = []
dj_admins= get_setting('DJANGO_ADMINS', 'django_admins', None)
if dj_admins:
    dj_admins=dj_admins.split(' ')
    for ad in dj_admins:
        ADMINS.append(ad.split(':'))

logger.debug('ADMINS :'+str(ADMINS))  


# for Fa Icon app
FAICON_YAML_FILE = str(STATICFILES_DIRS[0])+'/fontawesome/metadata/icons.yml'
# FAICON_CSS_URL = str(STATICFILES_DIRS[0])+'/fontawesome/css/all.css'
