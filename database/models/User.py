from database.connection import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, unique=True)
    user = Column(String(20), unique=True, nullable=False)
    username = Column(String(20), nullable=False)
    hashed_password = Column(String(120), nullable=False)