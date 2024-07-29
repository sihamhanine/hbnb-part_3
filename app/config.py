"""
Python module manage config app
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from dotenv import load_dotenv
from models import *
import os

db = SQLAlchemy()

# Generate and force directory for SQLite db
basedir = os.path.abspath(os.path.dirname(__file__))
datadir = os.path.join(basedir, 'data')
if not os.path.exists(datadir):
    os.makedirs(datadir)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Config:
    """
    Define Config class with development environment (Sqlite)
    or production environment (Postgresql)
    """
    if os.environ.get('FLASK_ENV') == 'production':
        load_dotenv('.env.prod')
        usr = os.environ.get('USERNAME')
        pwd = os.environ.get('PASSWORD')
        db_name = os.environ.get('DB_NAME')

        SQLALCHEMY_DATABASE_URI = f'postgresql://{usr}:{pwd}@127.0.0.1:5432/{db_name}'
        engine = create_engine(SQLALCHEMY_DATABASE_URI)

    elif os.environ.get('FLASK_ENV') == 'development':
        load_dotenv('.env.dev')
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
            os.path.join(datadir, 'development.db')
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
