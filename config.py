class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DNS_FORWARD_SUBMIT_PATH="/tmp/iwgweb.conf"

    LISTEN_HOST=""
    LISTEN_PORT=5001

    SECRET_KEY='123456790'
    DATABASE_FILE = 'iwg'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/' + DATABASE_FILE

    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """
    Production configurations
    """

    DNS_FORWARD_SUBMIT_PATH="/var/named/iwgweb.conf"

    LISTEN_HOST=""
    LISTEN_PORT=5000

    SECRET_KEY='123456790'
    DATABASE_FILE = 'iwg'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:iwgconf@localhost/' + DATABASE_FILE

    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app_config = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig
}
