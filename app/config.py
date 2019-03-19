import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'hard to guess string'
    SQLALCHEMY_DATABASE_URI = \
        'sqlite:///'+ os.path.join(basedir,'tracker.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  