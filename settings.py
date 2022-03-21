import os
import urllib


db_host_server = os.environ.get('DB_HOST', 'localhost')
db_server_port = urllib.parse.quote_plus(str(os.environ.get('DB_PORT', '5432')))
database_name = os.environ.get('DB_NAME', 'fastapi')
db_username = urllib.parse.quote_plus(str(os.environ.get('DB_USER', 'postgres')))
db_password = urllib.parse.quote_plus(str(os.environ.get('DB_PASSWORD', 'secret')))
ssl_mode = urllib.parse.quote_plus(str(os.environ.get('SSL_MODE', 'prefer')))
DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(
    db_username, db_password, db_host_server, db_server_port, database_name, ssl_mode
)

SECRET_KEY = os.environ.get('SECRET_KEY', 'SecretKey')
ALGORITHM = os.environ.get('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', 60)
SHORT_LINK_EXPIRE_DAYS = os.environ.get('SHORT_LINK_EXPIRE_DAYS', 1)
TIME_CHECK_EXPIRED_LINKS_SECONDS = os.environ.get('TIME_CHECK_EXPIRED_LINKS', 3600)
