## Synopsis

This module is an add-on for Django that provides Web-OIDC accounts management. It plays two roles:
- The Relying Party
- The Authentification provider

## Requirements

* djangoldp~=0.5
* validators~=0.12
* pyoic~=0.15
* django-oidc-provider~=0.6

## Installation

1. Install this module and all its dependencies

```
pip install djangoldp_account
```

2. Update settings.py on your server

```
DJANGOLDP_PACKAGES = [
    ...
    'djangoldp_account',
    ...
]
LOGIN_URL = '/accounts/login/'

OIDC_USERINFO = 'djangoldp_account.settings.userinfo'
OIDC_REGISTRATION_ENDPOINT_REQ_TOKEN = False

AUTHENTICATION_BACKENDS = [...,'djangoldp_account.auth.backends.ExternalUserBackend']
```

## Authenticate from an external provider

- go to mysite.org/accounts/login
- On the second form, put your email (me@theothersite.com) or the Authorization server url (https://theothersite.com/openid) 

Note: The url provided must contains /openid-configuration (for instance : https://theothersite.com/openid/openid-configuration must exists)

Once authentication on theothersite.com an account will be create on mysite.org and you'll be authentified both on theothersite.com and on mysite.com. 

## How to know a user is authenticated

When a user is authenticated on the server, any request will contains the header `User` with user webid
For instance :
```
GET https://mysite.com

HEADERS:
User: https://theothersite.com/users/2
```

Note that `GET https://mysite.com/user/1` will return something like :

```
HEADERS
User: https://anysite.com/users/X

BODY
{
  "@id": "https://theothersite.com/users/2",
  "first_name": "John",
}
```

Because `/user/1` is an account of an external user with webid `https://theothersite.com/users/2`  

# Extending User serialization

djangoldp_account use `django.contribs.auth.User` and mange its serialization into JsonLd format
If you need to extends it with you own relation use `USER_NESTED_FIELDS` on settings.py :

````
USER_NESTED_FIELDS=['skills']
```