from database.connection import Base
from sqlalchemy import Column, Integer, ForeignKey

class Request(Base):
    __tablename__ = 'requests'
    request_id = Column(Integer, primary_key=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    requested_id = Column(Integer, ForeignKey('users.id'), nullable=False)