from djangoldp.tests.settings_default import *

AUTH_USER_MODEL='djangoldp_account.LDPUser'

USER_ANONYMOUS_PERMISSIONS=['add', 'view']
USER_AUTHENTICATED_PERMISSIONS=['view', 'add']
USER_OWNER_PERMISSIONS=['view', 'add', 'change']
GROUP_ANONYMOUS_PERMISSIONS=['view']
GROUP_AUTHENTICATED_PERMISSIONS=['view', 'add', 'change']
GROUP_OWNER_PERMISSIONS=['view', 'add', 'change']

LOGIN_URL = '/auth/login/'
OIDC_USERINFO = 'djangoldp_account.settings.userinfo'
OIDC_REGISTRATION_ENDPOINT_REQ_TOKEN = False
OIDC_REGISTRATION_ENDPOINT_ALLOW_HTTP_ORIGIN = True
OIDC_IDTOKEN_SUB_GENERATOR = 'djangoldp_account.settings.sub_generator'
OIDC_IDTOKEN_EXPIRE = 60 * 60 * 1600

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'djangoldp_account.auth.middleware.JWTUserMiddleware'
]

AUTHENTICATION_BACKENDS = [
    'djangoldp_account.auth.backends.EmailOrUsernameAuthBackend',
    'guardian.backends.ObjectPermissionBackend',
    'djangoldp_account.auth.backends.ExternalUserBackend'
]

ANONYMOUS_USER_NAME = None

DJANGOLDP_PACKAGES=['djangoldp_account', 'djangoldp_account.tests']
INSTALLED_APPS=('django.contrib.auth',
               'django.contrib.contenttypes',
               'django.contrib.sessions',
               'django.contrib.admin',
               'guardian',
               'oidc_provider',
               'djangoldp_account',
               'djangoldp_account.tests',
               'djangoldp',
               )

LANGUAGE_CODE='en-us'
TIME_ZONE='UTC'
USE_I18N=True
USE_L10N=True
USE_TZ=True
EMAIL_ON_ACCOUNT_CREATION=False
JABBER_DEFAULT_HOST=None