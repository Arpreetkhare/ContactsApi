
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
