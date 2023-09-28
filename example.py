import sqlite3

# connecting with the database
connection = sqlite3.connect("data.db")

# object that can execute sql queries
cursor = connection.cursor()

# Query all Data
cursor.execute("SELECT * FROM events WHERE band='Tigers'")
rows=cursor.fetchall()
print(rows)

# Query certain columns
cursor.execute("SELECT band, date FROM events WHERE band='Tigers'")
rows=cursor.fetchall()
print(rows)

# INSERT new rows
new_rows=[('Cats', 'Cat City', '2088.10.17'), ('Dogs', 'DOg City', '2088.10.17'), ('Birds', 'Bird City', '2088.10.17')]
cursor.executemany("INSERT INTO events VALUES(?,?,?)",new_rows)

# Write the changes in the database
connection.commit()