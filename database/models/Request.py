from database.connection import db, Base

class Request(Base):
    __tablename__ = 'requests'
    request_id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    requested_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)