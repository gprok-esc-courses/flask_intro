import sqlite3

db = sqlite3.connect('mydb.sqlite3')

db.execute("""
    CREATE TABLE IF NOT EXISTS users 
    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
     username TEXT, 
     password TEXT)
""")

username = input("Username: ")
password = input("Password: ")

db.execute("INSERT INTO users (username, password) VALUES ('" + username + "', '" + password + "')" )

cursor = db.cursor()
result = cursor.execute("SELECT * FROM users")

print("USERS")
for row in result:
    print(str(row[0]) + ". " + row[1])

db.commit()