import sqlite3
conn=sqlite3.connect('test.db')
c=conn.cursor()

kitty=User(username='kitty')