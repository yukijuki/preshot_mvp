class Config(object):
    DEBUG = False
    Testing = False

    # SECRET_KEY = "super-secret"

    UPLOADS = "C:\\Users\\yukij\\Desktop\\Preshot\\static\\img"

    SESSION_COOKIE_SECURE = True

    SQLALCHEMY_TRACK_MODIFICATIONS = True

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    
    DB_NAME = "production-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "example"