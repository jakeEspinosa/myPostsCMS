from flask import Flask, request
from sqlalchemy import create_engine, Column, Integer, String, Text, select, insert
from sqlalchemy.engine import URL
from sqlalchemy.orm import deferred, DeclarativeBase
import os

app = Flask(__name__)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(30), unique=True)
    password = deferred(Column(String(255)))

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(255), nullable=False, unique=True)
    author = Column(String(50), nullable=False) 
    content = Column(Text, nullable=False, unique=True)

url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.environ['DB_USERNAME'],
    password=os.environ['DB_PASSWORD'],
    host="localhost",
    database="posts",
)

engine = create_engine(url)
Base.metadata.create_all(engine)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/signup', methods = ['POST'])
def sign_up():
    data = request.json
    usernameRes = data.get('username')
    passwordRes = data.get('password')
    stmt = (
    insert(User).
    values(username=usernameRes, password=passwordRes)
    )
    with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()

    return "success"

if __name__ == '__main__':
    app.run()
