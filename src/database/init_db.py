import sqlite3

conn = sqlite3.connect('clubstat.db')
cur = conn.cursor()

with open('src/database/schema.sql', 'r', encoding='utf-8') as f:
    sql_script = f.read()

cur.executescript(sql_script)

conn.commit()
conn.close()
