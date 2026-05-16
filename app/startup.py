import sqlite3
import os
import datetime

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/sample.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS cells (
        id INTEGER PRIMARY KEY,
        cell_name TEXT,
        traffic INTEGER,
        date TEXT
    )''')

    # Check if data exists already
    count = conn.execute("SELECT COUNT(*) FROM cells").fetchone()[0]
    if count == 0:
        # Insert sample data
        for i in range(7):
            date = (datetime.date.today() - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
            conn.execute(f"INSERT INTO cells VALUES (NULL, 'Cell_A', 0, '{date}')")
            conn.execute(f"INSERT INTO cells VALUES (NULL, 'Cell_B', {200 + i*10}, '{date}')")
            conn.execute(f"INSERT INTO cells VALUES (NULL, 'Cell_C', {0 if i < 3 else 180}, '{date}')")
            conn.execute(f"INSERT INTO cells VALUES (NULL, 'Cell_D', {350 + i*5}, '{date}')")
            conn.execute(f"INSERT INTO cells VALUES (NULL, 'Cell_E', {0 if i % 2 == 0 else 120}, '{date}')")

    conn.commit()
    conn.close()
    print("Database initialized!")

if __name__ == "__main__":
    init_db()
