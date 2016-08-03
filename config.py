from os import environ


class Config(object):
    PORT = 5000
    HOST = "0.0.0.0"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///wigle.db'


class DEV(Config):
    DEBUG = True


settings = globals()[environ.get('FASTER_CONFIG', 'DEV')]
