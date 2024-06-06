from pathlib import Path

from decouple import config

DIR = Path(__file__).absolute().parent

BOT_TOKEN = config('BOT_TOKEN')
TELEGRAM_TEST_SERVER = config('TELEGRAM_TEST_SERVER', default=False, cast=bool)
ADMINS = config('ADMINS', default='').split(',')
RATE_LIMIT = config('RATE_LIMIT', default=0.5, cast=float)

DB_USER = config('DATABASE_USER', default=None)
DB_PASSWORD = config('DATABASE_PASS', default=None)
DB_HOST = config('DATABASE_HOST', default=None)
DB_PORT = config('DATABASE_PORT', default=5432, cast=int)
DB_NAME = config('DATABASE_NAME', default=None)

REDIS_HOST = config('REDIS_HOST', default=None)
REDIS_PORT = config('REDIS_PORT', default=6379, cast=int)
REDIS_DB = config('REDIS_DB', default=5, cast=int)

WEBHOOK_PORT = config('WEBHOOK_PORT', default=8000)
WEBHOOK_HOST = config('WEBHOOK_HOST', default=None)
WEBHOOK_PATH = config('WEBHOOK_PATH', default=None)


MINSCOREFORBUDGET126 = config('MINSCOREFORBUDGET126', default=None, cast=float)
MINSCOREFORBUDGET172 = config('MINSCOREFORBUDGET172', default=None, cast=float)


I18N_DEFAULT_LOCALE = config('I18N_DEFAULT_LOCALE', default='en')
I18N_DOMAIN = 'bot'
LOCALES_DIR = f'{DIR}/locales'


# NMT
nmt_24_172 = {
    1: {
        "subject": "Українська мова(Ukrainian)",
        "weight": 0.3
    },
    2: {
        "subject": "Математика(Math)",
        "weight": 0.5
    },
    3: {
        "subject": "Історія України(History)",
        "weight": 0.2
    },
    4: [
        {
            "subject": "Іноземна мова(Foreign)",
            "weight": 0.25
        },
        {
            "subject": "Біологія(Biology)",
            "weight": 0.2
        },
        {
            "subject": "Фізика(Physics)",
            "weight": 0.5
        },
        {
            "subject": "Хімія(Chemistry)",
            "weight": 0.2
        },
        {
            "subject": "Українська література(Ukrainian literature)",
            "weight": 0.2
        },
        {
            "subject": "Географія(Geography)",
            "weight": 0.2
        }
    ]
}

nmt_24_126 = {
    1: {
        "subject": "Українська мова(Ukrainian)",
        "weight": 0.3
    },
    2: {
        "subject": "Математика(Math)",
        "weight": 0.5
    },
    3: {
        "subject": "Історія України(History)",
        "weight": 0.2
    },
    4: [
        {
            "subject": "Іноземна мова(Foreign)",
            "weight": 0.3
        },
        {
            "subject": "Біологія(Biology)",
            "weight": 0.2
        },
        {
            "subject": "Фізика(Physics)",
            "weight": 0.4
        },
        {
            "subject": "Хімія(Chemistry)",
            "weight": 0.2
        },
        {
            "subject": "Українська література(Ukrainian literature)",
            "weight": 0.2
        },
        {
            "subject": "Географія(Geography)",
            "weight": 0.2
        }
    ]
}
