import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from db import engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'users_cli'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    salt = Column(String(64), nullable=False)
    password_hash = Column(String(128), nullable=False)
    recommendations = relationship("UserRecommendation", back_populates="user")


class UserRecommendation(Base):
    __tablename__ = 'user_recommendations'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users_cli.id'), nullable=False)
    movie_id = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    overview = Column(Text, nullable=True)
    release_date = Column(String(20), nullable=True)
    poster_path = Column(String(255), nullable=True)
    watch_providers = Column(Text, nullable=True)  # JSON string
    trailer_url = Column(String(500), nullable=True)
    recommended_at = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship("User", back_populates="recommendations")

# Create tables if they don't exist
Base.metadata.create_all(engine)
