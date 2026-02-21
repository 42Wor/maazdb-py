
# MaazDB-Py 🐍

**The Official Python Driver for MaazDB**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![Security](https://img.shields.io/badge/security-TLS_1.3-green)
[![Website](https://img.shields.io/badge/Website-maazdb.vercel.app-blueviolet)](https://maazdb.vercel.app/)

`maazdb-py` is a pure-Python client library for interacting with the MaazDB engine. It implements the custom MaazDB binary protocol over a secure TLS 1.3 socket, allowing Python applications to communicate with your database safely and efficiently.

---

## ✨ Features

- **Secure by Default:** Automatic TLS 1.3 encryption for all communications.
- **Pure Python:** No heavy C-extensions; easy to install and cross-platform.
- **Context Manager Support:** Use `with` statements for safe connection handling.
- **Binary Protocol:** Optimized communication using the MaazDB Binary Protocol v1.
- **Lightweight:** Minimal dependencies.

---

## 📦 Installation

### From PyPI
```bash
pip install maazdb-py
```

### From Source
```bash
git clone https://github.com/42Wor/maazdb-py.git
cd maazdb-py
pip install .
```

---

## 🛠 Quick Start

### Basic Usage
```python
from maazdb import MaazDB

# 1. Initialize the client
db = MaazDB()

try:
    # 2. Connect securely
    db.connect(host="127.0.0.1", port=8888, user="admin", password="password")
    print("✓ Connected to MaazDB")

    # 3. Execute SQL
    db.query("CREATE DATABASE analytics;")
    db.query("USE analytics;")
    db.query("CREATE TABLE logs (id SERIAL PRIMARY KEY, message TEXT);")
    
    # 4. Insert and Fetch
    db.query("INSERT INTO logs (message) VALUES ('System started');")
    results = db.query("SELECT * FROM logs;")
    print(f"Results:\n{results}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # 5. Always close the connection
    db.close()
```

### Using Context Managers (Recommended)
The driver supports the `with` statement, which automatically closes the connection even if an error occurs.

```python
from maazdb import MaazDB

with MaazDB() as db:
    db.connect("127.0.0.1", 8888, "admin", "admin")
    result = db.query("SELECT count(*) FROM users;")
    print(f"Total users: {result}")
```

---

## 📋 API Reference

### `MaazDB()`
The main class to interact with the database.

- **`.connect(host, port, user, password)`**: Establishes a TLS 1.3 connection and performs the handshake.
- **`.query(sql_string)`**: Sends a SQL query to the server and returns the result as a string.
- **`.close()`**: Safely closes the socket connection.

---

## 🔐 Security & Protocol

The driver communicates using the **MaazDB Binary Protocol v1**. All data is packed as **Big Endian** (`>I`).

| Step | Type | Description |
| :--- | :--- | :--- |
| **Handshake** | `0x10` | `[Type] [Len] [User\0Pass\0Signature]` |
| **Query** | `0x20` | `[Type] [Len] [SQL String]` |
| **Success** | `0x02` | `[Type] [Len] [Result Data]` |
| **Error** | `0x03` | `[Type] [Len] [Error Message]` |

---

## 👩‍💻 Development & Contributing

If you are interested in contributing to the driver or building from source, please refer to the [DEVELOPER.md](./DEVELOPER.md) file for:
- Project structure
- Setting up a development environment
- Building and publishing to PyPI

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---
*Created for the [MaazDB Ecosystem](https://maazdb.vercel.app/).*
