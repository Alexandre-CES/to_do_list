from database.connection import db, Base
from datetime import datetime

class Task(Base):
    __tablename__ = 'tasks'
    task_id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    task = db.Column(db.String(42), nullable=False)
    description = db.Column(db.String(245))
    start = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ending = db.Column(db.DateTime, nullable=True)