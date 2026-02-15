# MaazDB-Py 🐍

**The Official Python Driver for MaazDB**

[🌐 Official Website](https://maazdb.vercel.app/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![Security](https://img.shields.io/badge/security-TLS_1.3-green)

`maazdb-py` is a pure-Python client library for interacting with the MaazDB engine. It implements the custom MaazDB binary protocol over a secure TLS 1.3 socket, allowing Python applications to communicate with your database safely and efficiently.

## ⚙️ Compatibility

This library is designed to work with:
*   **MaazDB Server:** Version `v12.0.0` and above.

## 📦 Installation

You can install the driver directly from the source code:

```bash
git clone https://github.com/42Wor/maazdb-py.git
cd maazdb-py
pip install .
```

## 🛠 Usage

### Basic Connection

```python
from maazdb import MaazDB

# 1. Initialize the client
db = MaazDB()

try:
    # 2. Connect securely (TLS is handled automatically)
    db.connect("127.0.0.1", 8888, "admin", "admin")
    print("✓ Connected to MaazDB")

    # 3. Run SQL commands
    db.query("CREATE DATABASE analytics;")
    db.query("USE analytics;")
    
    # 4. Insert Data
    db.query("CREATE TABLE visits (id SERIAL PRIMARY KEY, ip TEXT);")
    db.query("INSERT INTO visits (ip) VALUES ('192.168.1.1');")

    # 5. Fetch Results
    results = db.query("SELECT * FROM visits;")
    print(f"Results:\n{results}")

except Exception as e:
    print(f"Error: {e}")

finally:
    # 6. Close connection
    db.close()
```

### Using Context Managers (Recommended)

The driver supports the `with` statement, which automatically closes the connection even if errors occur.

```python
from maazdb import MaazDB

with MaazDB() as db:
    db.connect("127.0.0.1", 8888, "admin", "admin")
    
    result = db.query("SELECT count(*) FROM users;")
    print(result)
# Connection is automatically closed here
```

## 📋 Protocol Specifications

The driver communicates using the **MaazDB Binary Protocol v1**:

1.  **Handshake:** `[Type: 0x10] [Len: 4B] [User\0Pass\0Sig]`
2.  **Query:** `[Type: 0x20] [Len: 4B] [SQL String]`
3.  **Response:** `[Type: 0x02/0x03] [Len: 4B] [Result String]`

All integers are packed as **Big Endian** (`>I` in Python `struct`).

## 🧪 Development

To run the included example script:

1.  Ensure your **MaazDB Server** (v12.0.0+) is running on port 8888.
2.  Run the example:

```bash
python examples/basic.py
```

## 📄 License

Distributed under the MIT License.

---
*Created for the MaazDB Ecosystem.*