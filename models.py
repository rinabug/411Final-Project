# models.py
from flask_sqlalchemy import SQLAlchemy
from bcrypt import hashpw, gensalt, checkpw

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(32), nullable=False)

    @staticmethod
    def create_user(username, password):
        salt = gensalt().decode()
        hashed_pw = hashpw(password.encode(), salt.encode()).decode()
        user = User(username=username, password_hash=hashed_pw, salt=salt)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def verify_user(username, password):
        user = User.query.filter_by(username=username).first()
        if not user:
            return False
        return checkpw(password.encode(), user.password_hash.encode())
