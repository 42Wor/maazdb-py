# FILE PATH: examples/cli.py

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
        print("✓ Connected via TLS 1.3")
        print("Type 'exit' to quit.\n")

        while True:
            try:
                sql = input("maazdb> ").strip()

                if not sql:
                    continue

                if sql.lower() in ("exit", "quit"):
                    break

                result = db.query(sql)
                print(f"Server:\n{result.strip()}\n")

            except KeyboardInterrupt:
                print("\nInterrupted.")
                break

    except MaazDBError as e:
        print(f"❌ Error: {e}")

    finally:
        db.close()
        print("Connection closed.")


if __name__ == "__main__":
    main()
