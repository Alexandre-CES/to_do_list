from database.connection import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

class Task(Base):
    __tablename__ = 'tasks'
    task_id = Column(Integer, primary_key=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    priority = Column(Integer, nullable=False)
    task = Column(String(42), nullable=False)
    description = Column(String(245))
    start = Column(DateTime, default=datetime.now(), nullable=False)
    ending = Column(DateTime, nullable=True)