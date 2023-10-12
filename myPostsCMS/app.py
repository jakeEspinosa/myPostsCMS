from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Text, insert, select, LargeBinary
from sqlalchemy.engine import URL
from sqlalchemy.orm import deferred, DeclarativeBase
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import bcrypt
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
    password = Column(LargeBinary, nullable=False)
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

username1 = os.environ['ACCT_USERNAME']

with engine.connect() as conn:
    for row in conn.execute(select(User).filter_by(username=username1)):
        result = row._asdict()
        if result:
            break
        else:
            stmt = (
                insert(User).
                values(username=os.environ['ACCT_USERNAME'],
                password=bcrypt.hashpw(bytes(os.environ['ACCT_PASSWORD'], 'utf-8'), bcrypt.gensalt()),
                email=os.environ['ACCT_EMAIL'])
                )
        conn.execute(stmt)
        conn.commit()

@app.route('/login', methods = ['POST'])
def login():
    data = request.json
    passwordRes = data.get('password')
    passwordResBytes = bytes(passwordRes, 'utf-8')
    emailRes = data.get('email')
    with engine.connect() as conn:
        for row in conn.execute(select(User).filter_by(email=emailRes)):
            result = row._asdict()
    if bcrypt.checkpw(passwordResBytes, result['password']):
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

@app.route('/posts')
def get_posts():
    result = []
    with engine.connect() as conn:
        for id in conn.execute(select(User.id)):
            result.append(id._asdict())
    return jsonify(posts=result)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
