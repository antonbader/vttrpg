import sqlite3
import os

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'ttrpg.db')

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if 'order' column exists in 'adventure' table
    cursor.execute("PRAGMA table_info(adventure)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'order' not in columns:
        print("Adding 'order' column to 'adventure' table...")
        cursor.execute("ALTER TABLE adventure ADD COLUMN `order` INTEGER DEFAULT 0")

    # Check if 'order' column exists in 'scene' table
    cursor.execute("PRAGMA table_info(scene)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'order' not in columns:
        print("Adding 'order' column to 'scene' table...")
        cursor.execute("ALTER TABLE scene ADD COLUMN `order` INTEGER DEFAULT 0")

    conn.commit()
    conn.close()
    print("Migration complete.")
else:
    print(f"Database not found at {db_path}. Assuming it will be created with the new schema.")
