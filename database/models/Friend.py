from database.connection import Base
from sqlalchemy import Column, Integer, ForeignKey

class Friend(Base):
    __tablename__ = 'friends'
    friendship_id = Column(Integer, primary_key=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    friend_id = Column(Integer, ForeignKey('users.id'), nullable=False)    