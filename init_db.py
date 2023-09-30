import os
import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="posts",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS posts;')
cur.execute('CREATE TABLE posts (id serial PRIMARY KEY,'
                                 'title varchar (255) NOT NULL,'
                                 'author varchar (50) NOT NULL,'
                                 'content text,'
                                 'is_published boolean DEFAULT false,'
                                 'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                 )

# Insert data into the table
cur.execute('INSERT INTO posts (title, author, content)'
            'VALUES (%s, %s, %s)',
            ('DSA',
             'Jake Espinosa',
             'A great classic!')
            )

# Create users table
cur.execute('DROP TABLE IF EXISTS users;')
cur.execute('CREATE TABLE users (id serial PRIMARY KEY,'
                                 'username varchar (255) UNIQUE NOT NULL,'
                                 'password varchar (255) NOT NULL,'
                                 'is_disabled boolean DEFAULT false NOT NULL);'
                                 )

conn.commit()

cur.close()
conn.close()