import sqlite3

conn = sqlite3.connect("finance.db")
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
conn.close()

print("Tabele în finance.db:", tables)
