from database.connection import db, Base

class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    hashed_password = db.Column(db.String(120), nullable=False)