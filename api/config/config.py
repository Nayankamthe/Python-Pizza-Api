import os
from decouple import config
from datetime import timedelta

BASE_DIR =os.path.dirname(os.path.realpath(__file__))
# # to set FLASK_APP = api/  as enviornment variable in project.
# FLASK_APP = config('FLASK_APP')
# print(f'FLASK_APP value: {FLASK_APP}')

# postgress horuku deployment.
uri = config("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgress://","postgresql://",1)

class Config:
    SECRET_KEY = config('SECRET_KEY','secret')
    SQLALCHEMY_TRACK_MODIFICATION =False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')
    
class DevConfig(Config):
    DEBUG = config('DEBUG',cast=bool)
    SQLALCHEMY_ECHO =True
    SQLALCHEMY_DATABASE_URI ='sqlite:///'+os.path.join(BASE_DIR,'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATION=False
class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATION=False
    DEBUG = config('DEBUG', cast= bool)

class TestConfig(Config):
    TESTING =True
    SQLALCHEMY_ECHO =True
    SQLALCHEMY_DATABASE_URI ="sqlite:///"
    SQLALCHEMY_TRACK_MODIFICATION = False


config_dict= {
    'dev': DevConfig,
    'testing':TestConfig,
    'production':ProdConfig
    }