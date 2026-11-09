from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///instance/tdl.db', echo=True)
Base = declarative_base()
db = SQLAlchemy()