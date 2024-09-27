
from decouple import config
import pymysql

pymysql.install_as_MySQLdb()



JWT_SECRET_KEY = config('JWT_SECRET_KEY')

import os

import os  # Make sure to import the os module

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ContactApi',
        'USER': 'root',
        'PASSWORD': '1812',
        'HOST': 'mysql',  # The MySQL service hostname is the container name
        'PORT': '3306',
    }
}
