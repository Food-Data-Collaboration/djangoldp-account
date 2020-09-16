INSTALLED_APPS = [
    'oidc_provider'
]

MIDDLEWARE = [
    'djangoldp_account.auth.middleware.JWTUserMiddleware'
]

LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/redirect-default/'
OIDC_USERINFO = 'djangoldp_account.settings.userinfo'
OIDC_REGISTRATION_ENDPOINT_REQ_TOKEN = False
OIDC_REGISTRATION_ENDPOINT_ALLOW_HTTP_ORIGIN = True
OIDC_IDTOKEN_SUB_GENERATOR = 'djangoldp_account.settings.sub_generator'
OIDC_IDTOKEN_EXPIRE = 60 * 60 * 1600
AUTH_USER_MODEL = 'djangoldp_account.LDPUser'
