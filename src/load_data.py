import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

# CREATE_TABLE = " CREATE TABLE users (id int, email text, password text)"
#
# cursor.execute(CREATE_TABLE)
#
# user = (1,"test@gmail.com","root")
#
# INSERT_USER = "INSERT INTO users VALUES (?,?,?)"
#
# cursor.execute(INSERT_USER,user)
#
# users = [
#     (2,"hamza@gmail.com","root"),
#     (3,"mariam@gmail.com","root")
# ]
#
# cursor.executemany(INSERT_USER,users)
#
# SELECT_QUERY = "SELECT * FROM users"
#
# for record in cursor.execute(SELECT_QUERY):
#     print(record)

CREATE_TABLE = " CREATE TABLE items (id int, name text, price real)"

cursor.execute(CREATE_TABLE)

INSERT_ITEM = "INSERT INTO items VALUES (?,?,?)"

items = [
    (1,"belgha",120.00),
    (2,"9andoura",200.00)
]

cursor.executemany(INSERT_ITEM,items)

SELECT_QUERY = "SELECT * FROM items"

for record in cursor.execute(SELECT_QUERY):
    print(record)


connection.commit() #Essential
cursor.close() #Essential



