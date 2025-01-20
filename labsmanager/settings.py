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
from .config import get_setting, get_boolean_setting, get_media_dir, get_static_dir
import logging

from django.utils.translation import gettext_lazy as _

from .lab_version import *

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


logger.debug(f"=================================================================================")
logger.debug(f"                       LABSMANAGER / version {LABSMANAGER_VERSION}                  ")
logger.debug(f"=================================================================================")

logger.debug("-------------------------- Start debug session  --------------------------")

ALLOWED_HOSTS =  get_setting('DJANGO_ALLOWED_HOSTS', 'django_allowed_hosts', '*').split(" ") # ['*']  os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
logger.debug('ALLOWED_HOSTS :'+str(ALLOWED_HOSTS))   

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
    
    
    'django_extensions',
    
    'django_password_validators',   # https://pypi.org/project/django-password-validators/
    'django_password_validators.password_history',

    # Installed Package
    'crispy_forms',                 # https://django-crispy-forms.readthedocs.io/en/latest/install.html
    'crispy_bootstrap4',            # https://pypi.org/project/crispy-bootstrap4/
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
    'allauth',
    'allauth.account',              # https://django-allauth.readthedocs.io/en/latest/installation.html
    'invitations',                  # https://django-invitations.readthedocs.io
    'django_prose_editor',          # https://github.com/matthiask/django-prose-editor   rich text editor
    'rules.apps.AutodiscoverRulesConfig',       # https://pypi.org/project/rules/ For per object permission
    
    # App
    'staff.apps.StaffConfig',
    'project.apps.ProjectConfig',
    'fund.apps.FundConfig',
    'expense.apps.ExpenseConfig',
    'endpoints.apps.EndpointsConfig',
    'leave.apps.LeaveConfig',
    'reports.apps.ReportsConfig',
    'common.apps.CommonConfig',
    'settings.apps.SettingsConfig',
    'infos.apps.InfosConfig',
    'plugin.apps.PluginConfig',
    'notification.apps.NotificationConfig',
        
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]
MIDDLEWARE_CLASSES = (
    'labsmanager.UserEmployeeMiddleware',
)

MEDIA_ROOT = get_media_dir()
MEDIA_URL = 'media/'

# FOR CSP policies
use_csp = get_boolean_setting('ADMIN_USE_CSP', 'admin_use_csp', False)
logger.debug('CSP Policy enabled :'+str(use_csp))   
if use_csp:
    MIDDLEWARE+= ['csp.middleware.CSPMiddleware',]
    
    CSP_DEFAULT_SRC = ["'self'"]
    p=get_setting("ADMIN_CSP_DEFAULT",'admin_csp_default', None)
    if p is not None:
        CSP_DEFAULT_SRC+= p.split(",")
        
    CSP_BASE_URI = [] + CSP_DEFAULT_SRC
    p=get_setting("ADMIN_CSP_BASE_URI",'admin_csp_base_uri', None)
    if p is not None:
        CSP_BASE_URI +=  p.split(",")
    
    CSP_SCRIPT_SRC = [] + CSP_DEFAULT_SRC
    p=get_setting("ADMIN_CSP_SCRIPT",'admin_csp_script', None)
    if p is not None:
        CSP_SCRIPT_SRC +=  p.split(",")
    
    CSP_STYLE_SRC = [] + CSP_DEFAULT_SRC
    p=get_setting("ADMIN_CSP_STYLE",'admin_csp_style', None)
    if p is not None:
        CSP_STYLE_SRC +=  p.split(",") 
        
    CSP_FONT_SRC =[] +  CSP_DEFAULT_SRC
    p=get_setting("ADMIN_CSP_FONT",'admin_csp_font', None)
    if p is not None:
        CSP_FONT_SRC +=  p.split(",") 
    
    CSP_DATA_SRC  = [] + CSP_DEFAULT_SRC
    p=get_setting("ADMIN_CSP_DATA",'admin_csp_data', None)
    if p is not None:
        CSP_DATA_SRC +=  p.split(",") 
        
    CSP_IMG_SRC = [] + CSP_DEFAULT_SRC
    p=get_setting("ADMIN_CSP_IMG",'admin_csp_img', None)
    if p is not None:
        CSP_IMG_SRC +=  p.split(",") 
    
    CSP_MEDIA_SRC = [] + CSP_DEFAULT_SRC
    p=get_setting("ADMIN_CSP_MEDIA",'admin_csp_media', None)
    if p is not None:
        CSP_MEDIA_SRC +=  p.split(",")

    CSP_FRAME_ANCESTORS= [] #+ CSP_DEFAULT_SRC
    p=get_setting("ADMIN_CSP_FRAME_ANCESTORS",'admin_csp_frame_ancestors', None)
    if p is not None:
        CSP_FRAME_ANCESTORS +=  p.split(",")
    

logger.debug('=========  CSP PARAMETERS  =========')
logger.debug(f'  - CSP_DEFAULT_SRC: {CSP_DEFAULT_SRC}')
logger.debug(f'  - CSP_BASE_URI: {CSP_BASE_URI}')
logger.debug(f'  - CSP_SCRIPT_SRC: {CSP_SCRIPT_SRC}')
logger.debug(f'  - CSP_STYLE_SRC: {CSP_STYLE_SRC}')

logger.debug(f'  - CSP_FONT_SRC: {CSP_FONT_SRC}')
logger.debug(f'  - CSP_DATA_SRC: {CSP_DATA_SRC}')
logger.debug(f'  - CSP_IMG_SRC: {CSP_IMG_SRC}')
logger.debug(f'  - CSP_MEDIA_SRC: {CSP_MEDIA_SRC}')
logger.debug(f'  - CSP_FRAME_ANCESTORS: {CSP_FRAME_ANCESTORS}')
logger.debug('=========  =========  =========')

MIDDLEWARE +=[
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'auditlog.middleware.AuditlogMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
]
    
ROOT_URLCONF = 'labsmanager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                    MEDIA_ROOT.joinpath('report'),
                ],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries':{
                'customs_tags': 'labsmanager.templatetags.customs_tags',
                'lab_rules': 'labsmanager.templatetags.lab_rules',
                'format_tag': 'labsmanager.templatetags.format_tag',
                'plugin_tag': 'plugin.templatetags.plugin_tags',
            
            },
            'loaders': [
                (   'labsmanager.template.LabsManagerTemplateLoader',
                 [
                        'plugin.template.PluginTemplateLoader',
                        'django.template.loaders.filesystem.Loader',
                        'django.template.loaders.app_directories.Loader',
                    ],
                )
            ],
        },
    },
]

FIXTURE_DIRS =[
    os.path.join(BASE_DIR, 'labsmanager', 'fixtures'), 
    # BASE_DIR / "labsmanager" / "fixture",
]


LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

WSGI_APPLICATION = 'labsmanager.wsgi.application'




DATABASES = {
    'default': {
        'ENGINE': get_setting('SQL_ENGINE', 'sql_engine', 'django.db.backends.postgresql'),
        'NAME': get_setting('LAB_DB_NAME', 'lab_db_name', 'labsmanager'),
        'USER': get_setting('LAB_DB_USER', 'lab_db_user', 'labsmanager'), 
        'PASSWORD': get_setting('LAB_DB_PASSWORD', 'lab_db_password', 'labsManagerPass'),
        'HOST': get_setting('LAB_DB_HOST', 'lab_db_host', 'localhost'), 
        'PORT': get_setting('LAB_DB_PORT', 'lab_db_port', '5432'),
    }
}


AUTHENTICATION_BACKENDS = [
    'rules.permissions.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    ]
# accounts settings
ACCOUNT_DEFAULT_HTTP_PROTOCOL=get_setting('ACCOUNT_DEFAULT_HTTP_PROTOCOL', 'lab_default_http_protocol', 'http')
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE=False
ACCOUNT_CONFIRM_EMAIL_ON_GET=False

# allauth config
ACCOUNT_AUTHENTICATION_METHOD  = 'username_email'

ACCOUNT_SESSION_REMEMBER = False

ACCOUNT_ALLOW_SINGUP = get_boolean_setting('ACCOUNT_ALLOW_SINGUP', 'allow_sign_up', False)

# ACCOUNT_ADAPTER = 'labsmanager.labs_account_adaptater.LabsManagerAccountAdapter'
ACCOUNT_ADAPTER = "invitations.models.InvitationsAdapter" # for django-invitations

### Specific conf for django-invitations
INVITATIONS_ADAPTER = ACCOUNT_ADAPTER
INVITATIONS_ACCEPT_INVITE_AFTER_SIGNUP = True
INVITATIONS_INVITATION_ONLY = True

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 9,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'django_password_validators.password_history.password_validation.UniquePasswordsValidator',
        'OPTIONS': {
            'last_passwords': 5 # Only the last 5 passwords entered by the user
        }
    },
    {
        'NAME': 'django_password_validators.password_character_requirements.password_validation.PasswordCharacterValidator',
        'OPTIONS': {
             'min_length_digit': 1,
             'min_length_alpha': 1,
             'min_length_special': 1,
             'min_length_lower': 1,
             'min_length_upper': 1,
             'special_characters': "~!@#$%^&*()_+{}\":;'[]"
         }
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

STATIC_ROOT = get_static_dir() # '/home/labsmanager/data/static/'

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "data" / "static",
]

# Color Themes Directory
STATIC_COLOR_THEMES_DIR = os.path.join(STATIC_ROOT, 'css', 'color-themes')

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

ACCOUNT_FORMS = {
    'reset_password_from_key': 'common.forms.ResetLabPasswordKeyForm', 
    'signup': 'common.forms.LabSignupForm'       
    }
# Session 
SESSION_COOKIE_AGE = get_setting('LAB_SESSION_COOKIE_AGE', 'session_cookie_age', 6400)
# SESSION_COOKIE_NAME = '__Secure-sessionid'
# CSRF_COOKIE_NAME = '__Secure-csrftoken'

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
EMAIL_SUBJECT_PREFIX = get_setting('LAB_EMAIL_PREFIX', 'email.prefix', '[Labsmanager] ')
EMAIL_USE_TLS = get_boolean_setting('LAB_EMAIL_TLS', 'email.tls', False)
EMAIL_USE_SSL = get_boolean_setting('LAB_EMAIL_SSL', 'email.ssl', False)

DEFAULT_FROM_EMAIL = EMAIL_SENDER


# For Security design
CSRF_COOKIE_SECURE  = get_boolean_setting('CSRF_COOKIE_SECURE', 'csrf_cookie_secure', True)
CSRF_COOKIE_SAMESITE = get_setting('CSRF_COOKIE_SAMESITE', 'csrf_cookie_samesite', 'Strict')
SESSION_COOKIE_SECURE = get_boolean_setting('SESSION_COOKIE_SECURE', 'session_cookie_secure', True)
SECURE_BROWSER_XSS_FILTER = get_boolean_setting('SECURE_BROWSER_XSS_FILTER', 'secure_browser_xss_filter', True)
SECURE_CONTENT_TYPE_NOSNIFF = get_boolean_setting('SECURE_CONTENT_TYPE_NOSNIFF', 'secure_content_type_nosniff', True)
SECURE_SSL_REDIRECT =  get_boolean_setting('SECURE_SSL_REDIRECT', 'secure_ssl_redirect', True)
X_FRAME_OPTIONS =  get_setting('X_FRAME_OPTIONS', 'x_frame_options', 'DENY')
SECURE_HSTS_SECONDS = get_setting('SECURE_HSTS_SECONDS', 'secure_hsts_seconds', 300)
SECURE_HSTS_INCLUDE_SUBDOMAINS = get_boolean_setting('SECURE_HSTS_INCLUDE_SUBDOMAINS', 'secure_hsts_include_subdomains', True)
SECURE_HSTS_PRELOAD = get_boolean_setting('SECURE_HSTS_PRELOAD', 'secure_hsts_preload', True)

logger.debug('=========  SECURE PARAMETERS  =========')
logger.debug(f'  - USE CSP: {use_csp}')
logger.debug(f'  - SESSION_COOKIE_SECURE: {SESSION_COOKIE_SECURE}')
logger.debug(f'  - CSRF_COOKIE_SECURE: {CSRF_COOKIE_SECURE}')
logger.debug(f'  - SECURE_SSL_REDIRECT: {SECURE_SSL_REDIRECT}')

logger.debug(f'  - CSRF_COOKIE_SAMESITE: {CSRF_COOKIE_SAMESITE}')
logger.debug(f'  - SECURE_BROWSER_XSS_FILTER: {SECURE_BROWSER_XSS_FILTER}')
logger.debug(f'  - SECURE_CONTENT_TYPE_NOSNIFF: {SECURE_CONTENT_TYPE_NOSNIFF}')
logger.debug(f'  - X_FRAME_OPTIONS: {X_FRAME_OPTIONS}')
logger.debug(f'  - SECURE_HSTS_SECONDS: {SECURE_HSTS_SECONDS}')
logger.debug(f'  - SECURE_HSTS_INCLUDE_SUBDOMAINS: {SECURE_HSTS_INCLUDE_SUBDOMAINS}')
logger.debug(f'  - SECURE_HSTS_PRELOAD: {SECURE_HSTS_PRELOAD}')
logger.debug('=========  =========  =========')


# logger.debug(f'SECURE_SSL_REDIRECT: {SECURE_SSL_REDIRECT}')

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


ADMIN_HEADER =  get_setting('ADMIN_HEADER', 'admin_header', "LabsManager Admin")
ADMIN_SITE_TITLE =  get_setting('ADMIN_SITE_TITLE', 'admin_site_title', "LabsManager Admin")
ADMIN_INDEX_TITLE =  get_setting('ADMIN_INDEX_TITLE', 'admin_index_title', "Menu")

logger.debug('ADMIN_HEADER :'+str(ADMIN_HEADER))

logger.debug('ADMIN_SITE_TITLE :'+str(ADMIN_SITE_TITLE))

logger.debug('ADMIN_INDEX_TITLE :'+str(ADMIN_INDEX_TITLE))

logger.debug('=========  FOLDER PATH  =========')
logger.debug(f'  - BASE_DIR: {BASE_DIR}')
logger.debug(f'  - STATIC_URL: {STATIC_URL}')
logger.debug(f'  - STATIC_ROOT: {STATIC_ROOT}')
logger.debug(f'  - MEDIA_ROOT: {MEDIA_ROOT}')
logger.debug(f'  - STATICFILES_DIRS: {STATICFILES_DIRS}')
logger.debug(f'  - STATIC_COLOR_THEMES_DIR: {STATIC_COLOR_THEMES_DIR}')
logger.debug(f'  - FIXTURE_DIRS: {FIXTURE_DIRS}')
logger.debug('=========  =========  =========')


# For plugins 
PLUGINS_ENABLED = get_boolean_setting('LABSMANAGER_PLUGINS_ENABLED', 'plugin_enable', False)
TESTING = False
PLUGIN_TESTING = False
PLUGIN_TESTING_SETUP = False
PLUGIN_RETRY = True
PLUGIN_DIR = get_setting('LABSMANAGER_PLUGIN_DIR', 'plugin_dir')
TESTING_ENV = False
logger.debug('=========  Plugins  =========')
logger.debug(f'  - PLUGINS_ENABLED: {PLUGINS_ENABLED}')
logger.debug(f'  - PLUGIN_DIR: {PLUGIN_DIR}')
logger.debug(f'  - PLUGIN_TESTING: {PLUGIN_TESTING}')
logger.debug(f'  - PLUGIN_RETRY: {PLUGIN_RETRY}')
logger.debug('=========  =========  =========')

LABSMANAGER_SHOW_HELP=get_boolean_setting("LABSMANAGER_SHOW_HELP", 'show_help', True)
HELP_LINKS = []
help_lk= get_setting('HELP_LINK', 'help_link', None)
if help_lk:
    links=help_lk.split(' ')
    for link in links:
        label, url = link.split(';')
        HELP_LINKS.append({
            "label": _(label),
            "url": url,
        })
else:
    HELP_LINKS=[
            {
                "label":_("Documentation"),
                "url":"https://labsmanager-doc.readthedocs.io/en/latest/",
            },
            {
                "label":_("Issues"),
                "url":"https://github.com/Bbillyben/labsmanager/issues",
            },
        ]
