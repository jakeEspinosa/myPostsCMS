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
                                 'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                 )

# Insert data into the table

cur.execute('INSERT INTO posts (title, author, content)'
            'VALUES (%s, %s, %s)',
            ('DSA',
             'Jake Espinosa',
             'A great classic!')
            )

conn.commit()

cur.close()
conn.close()