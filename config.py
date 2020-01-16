class Config(object):
    DEBUG = False
    Testing = False
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
    app.config["SECRET_KEY"] = "superSecret"
    app.config["IMAGE_UPLOADS"] = "C:\\Users\\yukij\\Desktop\\preshot_mvp\\static\\img"
    app.config["UPLOAD_FOLDER"] = PHISICAL_ROOT + UPLOAD_FOLDER
    app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG", "JPEG", "GIF"]
    app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024

    SQLALCHEMY_TRACK_MODIFICATIONS = True

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    
    DB_NAME = "production-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "example"