
from decouple import config
import pymysql

pymysql.install_as_MySQLdb()



JWT_SECRET_KEY = config('JWT_SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ContactApi',
        'USER': 'dev_user',
        'PASSWORD': '1812',
        'HOST': 'localhost',  # Use MySQL container name, not 'localhost'
        'PORT': '3306',             # Default MySQL port
    }
}


import logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
        'authentication': {  # Replace with your app's name
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

