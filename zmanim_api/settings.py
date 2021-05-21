from os import environ

import sentry_sdk


I18N_DOMAIN = 'zmanim_api'
ROOT_PATH = environ.get('ROOT_PATH', '')
SENTRY_PUBLIC_KEY = environ.get('SENTRY_PUBLIC_KEY')


if SENTRY_PUBLIC_KEY:
    sentry_sdk.init(  # pragma: no cover
        dsn=SENTRY_PUBLIC_KEY
    )
