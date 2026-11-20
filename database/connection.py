from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///instance/tdl.db', echo=True)
Base = declarative_base()
db = SQLAlchemy()
