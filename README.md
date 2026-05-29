# MaazDB-Py 🐍

**The Official Python Driver for MaazDB**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![Security](https://img.shields.io/badge/security-TLS_1.3-green)
[![Website](https://img.shields.io/badge/Website-maazdb.vercel.app-blueviolet)](https://maazdb.vercel.app/)

`maazdb-py` is a pure-Python client library for interacting with the MaazDB engine. It implements the custom MaazDB Binary Protocol v2.1 over a secure TLS 1.3 socket, allowing Python applications to communicate with your database safely, securely, and efficiently.

---

## ✨ Features

- **Secure by Default:** TLS 1.3 socket wrapping for encrypted communication.
- **Cryptographic Handshake:** Implements the Protocol v2.1 challenge-response flow utilizing HMAC-SHA256 signatures to verify credentials without plaintext protocol exposure.
- **Latency-Optimized:** Disables Nagle's algorithm natively (`TCP_NODELAY`) to prevent OS-level packet buffering, reducing round-trip latency.
- **0-RTT Early Data Auto-Opt-In:** Automatically evaluates statements and tags read-only queries (`SELECT`, `SHOW`, `DESCRIBE`) with the `FLAG_EARLY_DATA` bitmask to execute safely during early TLS connection flights.
- **Context Manager Support:** Use `with` statements for safe, automated connection lifecycle management.
- **Pure Python:** No heavy C-extensions; lightweight with minimal dependencies.

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
    # 2. Connect securely (Handshake, HMAC signatures, and TCP_NODELAY are handled automatically)
    db.connect(host="127.0.0.1", port=8888, user="admin", password="admin")
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
The driver supports the `with` statement, which automatically closes the socket connection even if an error occurs.

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

- **`.connect(host, port, user, password)`**: Establishes a TLS 1.3 connection, configures TCP socket settings, and performs the challenge-response handshake.
- **`.query(sql_string)`**: Sends a SQL query to the server and returns the result as a string.
- **`.close()`**: Safely closes the socket connection.

---

## 🔐 Security & Protocol

The driver communicates using the **MaazDB Binary Protocol v2.1**. All integers are packed using Big Endian format (`>BBHI`). 

The 8-byte header structure is arranged as:
`[Type: 1B] [Flags: 1B] [Req ID: 2B] [Payload Length: 4B] [PayloadBytes]`

### Packet Type Mapping

| Step | Type (Hex) | Name | Description |
| :--- | :--- | :--- | :--- |
| **1. Challenge Request** | `0x10` | `CHALLENGE_REQ` | Sent by server containing 32-byte ephemeral random nonce. |
| **2. Challenge Response** | `0x11` | `CHALLENGE_RESP` | Sent by client with format: `Username\0Password\0DriverID\0SignatureHex`. |
| **3. Verification Success** | `0x12` | `AUTH_OK` | Sent by server confirming handshake and credentials. |
| **4. Verification Failure** | `0x13` | `AUTH_ERR` | Sent by server rejecting credentials or dropping session. |
| **5. Query Dispatch** | `0x20` | `QUERY` | Sent by client containing SQL query payload. |
| **6. Message Response** | `0x02` | `MSG_RESPONSE` | Sent by server containing execution status or response string. |
| **7. Data Response** | `0x03` | `DATA_RESPONSE` | Sent by server containing structured JSON columnar results. |

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
```