# FILE PATH: examples/basic.py
import sys
import os

# Add parent dir to path so we can import 'maazdb' without installing it via pip yet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from maazdb import MaazDB, MaazDBError

def main():
    print("--- MaazDB Python Client ---")
    
    db = MaazDB()

    try:
        # 1. Connect
        print("Connecting...")
        db.connect("127.0.0.1", 8888, "admin", "admin")
        print("✓ Connected via TLS")

        # 2. Run Queries
        queries = [
            "CREATE DATABASE py_test;",
            "USE py_test;",
            "CREATE TABLE python_users (id SERIAL PRIMARY KEY, name TEXT);",
            "INSERT INTO python_users (name) VALUES ('Guido');",
            "INSERT INTO python_users (name) VALUES ('Maaz');",
            "SELECT * FROM python_users;"
        ]

        for sql in queries:
            print(f"\nExecuting: {sql}")
            result = db.query(sql)
            print(f"Server: {result.strip()}")

    except MaazDBError as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()
        print("\nConnection closed.")

if __name__ == "__main__":
    main()