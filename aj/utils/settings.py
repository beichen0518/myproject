import os

from utils.functions import get_db_uri


BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

templates_dir = os.path.join(BASEDIR, 'templates')
static_dir = os.path.join(BASEDIR, 'static')

DATABASE = {
    'USER': 'root',
    'PASSWORD': '123456',
    'HOST': '127.0.0.1',
    'PORT': '3306',
    'DB': 'mysql',
    'DRIVER': 'pymysql',
    'NAME': 'aijia'
}

SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE)

UPLOAD_DIRS = os.path.join(os.path.join(BASEDIR, 'static'), 'upload')
