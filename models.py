from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import deferred, DeclarativeBase

Base = DeclarativeBase()

class User(Base):
    __tablename__ = 'users'
    Column('id', Integer, primary_key=True, nullable=False)
    Column('username', String(30), unique=True)
    deferred(Column('password', String(255)))

class Post(Base):
    __tablename__ = 'posts'
    Column('id', Integer, primary_key=True, nullable=False)
    Column('title', String(255), nullable=False, unique=True)
    Column('author', String(50), nullable=False) 
    Column('content', Text, nullable=False, unique=True)
    Column('version', Integer)
    Column('is_published', Boolean, nullable=False, default=1) 
    Column('date_published', DateTime, nullable=False)