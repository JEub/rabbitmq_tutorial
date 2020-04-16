import os
import dotenv

# setting directories
CONFIGDIR = os.path.dirname(os.path.abspath(__file__))
BASEDIR = os.path.dirname(CONFIGDIR)
ENV = os.path.join(BASEDIR, '.env')

# Loading a local environment if one exists
if os.path.exists(ENV):
    dotenv.load_dotenv(ENV)

environment = {
    'DB_USER': os.environ.get('DB_USER', 'postgres'),
    'DB_PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
    'DB_HOST': os.environ.get('DB_HOST', 'localhost'),
    'DB_PORT': os.environ.get('DB_PORT', 5432),
    'DB_DB': os.environ.get('DB_DB', 'postgres'),
    'RABBIT_MQ_USER': os.environ.get('RABBIT_MQ_USER', 'guest'),
    'RABBIT_MQ_PASSWORD':
        os.environ.get('RABBIT_MQ_PASSWORD', 'guest'),
    'RABBIT_MQ_BROKER':
        os.environ.get('RABBIT_MQ_BROKER', 'guest'),
}


class BaseConfig():
    API_PREFIX = '/api'
    TESTING = False
    DEBUG = False


class DevConfig(BaseConfig):
    FLASK_ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{environment['DB_USER']}"
        f":{environment['DB_PASSWORD']}"
        f"@{environment['DB_HOST']}"
        f":{environment['DB_PORT']}/"
        f"{environment['DB_DB']}"
    )
    CELERY_BROKER = (
        f"pyamqp://{environment['RABBIT_MQ_USER']}""
        f":{environment['RABBIT_MQ_PASSWORD']}"
        f"@{environment['RABBIT_MQ_BROKER']}//"
    )
    CELERY_RESULT_BACKEND = (
        f"{environment['RABBIT_MQ_USER']}"
        f":{environment['RABBIT_MQ_PASSWORD']}"
        f"@{environment['RABBIT_MQ_BROKER']}//"
    )


class ProductionConfig(BaseConfig):
    FLASK_ENV = 'production'
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{environment['DB_USER']}"
        f":{environment['DB_PASSWORD']}"
        f"@{environment['DB_HOST']}"
        f":{environment['DB_PORT']}/"
        f"{environment['DB_DB']}"
    )
    CELERY_BROKER = (
        f"pyamqp://{environment['RABBIT_MQ_USER']}""
        f":{environment['RABBIT_MQ_PASSWORD']}"
        f"@{environment['RABBIT_MQ_BROKER']}//"
    )
    CELERY_RESULT_BACKEND = (
        f"{environment['RABBIT_MQ_USER']}"
        f":{environment['RABBIT_MQ_PASSWORD']}"
        f"@{environment['RABBIT_MQ_BROKER']}//"
    )


class TestConfig(BaseConfig):
    FLASK_ENV = 'development'
    TESTING = True
    DEBUG = True
    # make celery execute tasks synchronously in the same process
    CELERY_ALWAYS_EAGER = True
