import os


class Config:
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@localhost:3306/FlaskTpp"
    SECRET_KEY = "Xtian"


ADMINS = {'ct', 'XTian'}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILE_PATH_PREFIX = "/static/uploads/icons"

UPLOADS_DIR = os.path.join(BASE_DIR, 'App/static/uploads/icons')