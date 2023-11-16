import os
import sqlite3

# Check if the SQLite database already exists and delete it
database_name = 'Temoa_Europe.sqlite'
if os.path.exists(database_name):
    os.remove(database_name)
    print('\n'f"Existing {database_name} database deleted.\n")

# Connect to the SQLite database
conn = sqlite3.connect(database_name)
cursor = conn.cursor()

# Execute the SQL script
sql_file_path = 'Temoa_Europe.sql'
with open(sql_file_path, 'r') as sql_file:
    sql_script = sql_file.read()

try:
    cursor.executescript(sql_script)

except sqlite3.Error as e:
    print('Error occurred during SQL execution:')
    print(str(e))

conn.commit()
conn.close()

# Continue with the rest of the code
print('SQLite database created and filled according to the SQL code.\n')

with open("database_preprocessing.py") as preprocessing:
    exec(preprocessing.read())
