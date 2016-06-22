import os


class Config(object):
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False
    CSRF_ENABLED = True

    SECRET_KEY = os.environ.get("SECRET_KEY", "super secret key")
    SUPER_SECRET_KEY = os.environ.get("SUPER_SECRET_KEY", "superer_secret_key")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "postgresql://localhost/arxivmail"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY", None)


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
