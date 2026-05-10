import sqlite3
import os

def verify():
    db_path = os.path.join('data', 'jp_game.db')
    if not os.path.exists(db_path):
        print("Database file not found.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM vocabulary")
    count = cursor.fetchone()[0]
    
    cursor.execute("SELECT * FROM vocabulary LIMIT 5")
    samples = cursor.fetchall()
    
    print(f"Total words in DB: {count}")
    print("Sample data:")
    for s in samples:
        print(s)
    
    conn.close()

if __name__ == "__main__":
    verify()