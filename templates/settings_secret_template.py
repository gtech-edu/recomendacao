#coding: utf-8

from {{ DOCKYARD_PKG }}.const import APP_NAME


# Fill the settings below with the correct values
# and save this file as "settings_secret.py"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '{{ SECRET_SECRET_KEY }}' # This should be set to a unique, unpredictable value

EMAIL_USE_TLS = True
EMAIL_HOST = '{{ SECRET_EMAIL_HOST }}'
EMAIL_PORT = {{ SECRET_EMAIL_PORT }}

EMAIL_HOST_USER = '{{ SECRET_EMAIL_HOST_USER }}'
EMAIL_HOST_PASSWORD = '{{ SECRET_EMAIL_HOST_PASSWORD | default() }}'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    ('Alisson Müller', 'alissonmller@gmail.com'),
)
MANAGERS = ADMINS
SERVER_EMAIL = 'django@' + APP_NAME + '.com'
