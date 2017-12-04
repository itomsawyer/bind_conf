class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    SECRET_KEY='123456790'
    DATABASE_FILE = 'iwg'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/' + DATABASE_FILE
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False

app_config = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig
}
