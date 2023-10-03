from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Text, insert, select
from sqlalchemy.engine import URL
from sqlalchemy.orm import deferred, DeclarativeBase
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import os

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ['SECRET_KEY']
jwt = JWTManager(app)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(30), unique=True, nullable=False)
    password = deferred(Column(String(255), nullable=False))
    email = Column(String(255), unique=True, nullable=False)

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

@app.route('/signup', methods = ['POST'])
def sign_up():
    data = request.json
    usernameRes = data.get('username')
    if usernameRes != 'jake':
        return "Sorry, only jake can make an account!", 401
    passwordRes = data.get('password')
    emailRes = data.get('email')
    stmt = (
    insert(User).
    values(username=usernameRes, password=passwordRes, email=emailRes)
    )
    with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()

    return "success"

@app.route('/login', methods = ['POST'])
def login():
    data = request.json
    passwordRes = data.get('password')
    emailRes = data.get('email')
    with engine.connect() as conn:
        user = conn.execute(select(User).filter_by(email=emailRes, password=passwordRes))
    if user:
        access_token = create_access_token(identity=emailRes)
        return jsonify(message='Login Successful', access_token=access_token)
    else:
        return jsonify('Bad email or Password'), 401

@app.route('/posts', methods = ['POST'])
@jwt_required()
def create_post():
    data = request.json
    titleRes = data.get('title')
    authorRes = data.get('author')
    contentRes = data.get('content')

    stmt = (
    insert(Post).
    values(title=titleRes, author=authorRes, content=contentRes)
    )
    with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()

    return "inserted"

if __name__ == '__main__':
    app.run()
