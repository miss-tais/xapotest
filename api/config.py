import os


def get_mysql_db_url(db_user, db_password, db_database, db_server):
    return f"mysql+pymysql://{db_user}:{db_password}@{db_server}/{db_database}"


class Config:
    """Flask configuration."""

    # General
    DEBUG = False
    TESTING = False

    SECRET_KEY = os.environ.get('SECRET_KEY', None)

    # Restful
    BUNDLE_ERRORS = True

    # Database
    db_user = os.environ.get("MYSQL_USER", "")
    db_password = os.environ.get("MYSQL_PASSWORD", "")
    db_database = os.environ.get("MYSQL_DATABASE", "")
    db_server = os.environ.get("MYSQL_SERVER", "")
    db_url = get_mysql_db_url(db_user, db_password, db_database, db_server)

    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", db_url)
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", False)

    OER_API_KEY = os.environ.get('OER_API_KEY', '')
    OER_BASE = os.environ.get('OER_BASE', 'USD')


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'development_config_secret'


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'test_config_secret'
    SQLALCHEMY_DATABASE_URI = get_mysql_db_url("test_db_user", 'test_db_password', 'test_db', '0.0.0.0:3307')


app_config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'test': TestingConfig
}
