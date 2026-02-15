


# 🛠 MaazDB-Py Developer Guide

This document contains instructions for developers working on the `maazdb-py` driver.

## 📂 Project Structure

```text
C:.
│   README.md           # Public documentation
│   DEVELOPER.md        # This file
│   setup.py            # Package configuration
│
├───maazdb              # Core Source Code
│   │   client.py       # Main MaazDB class
│   │   protocol.py     # Binary protocol implementation
│   │   exceptions.py   # Custom error classes
│   │   __init__.py     # Package entry point
│
├───examples            # Test scripts
│       basic.py
│       cli.py
```

## ⚙️ Development Setup

1. **Clone and Create Virtual Env:**
   ```bash
   git clone https://github.com/42Wor/maazdb-py.git
   cd maazdb-py
   python -m venv venv
   source venv/bin/activate  # Windows: .\venv\Scripts\activate
   ```

2. **Install in Editable Mode:**
   This allows you to test changes to the code immediately without reinstalling.
   ```bash
   pip install -e .
   ```

## 📦 Building & Publishing

To release a new version to PyPI:

1. **Update Version:** Change the version number in `setup.py`.
2. **Build the Package:**
   ```bash
   pip install --upgrade build twine
   python -m build
   ```
3. **Upload to PyPI:**
   ```bash
   python -m twine upload dist/*
   ```

## 📋 Protocol Specifications (v1)

The driver communicates using the **MaazDB Binary Protocol**:

- **Handshake (0x10):** `[Type: 1B] [Len: 4B] [User\0Pass\0Sig]`
- **Query (0x20):** `[Type: 1B] [Len: 4B] [SQL String]`
- **Response (0x02/0x03):** `[Type: 1B] [Len: 4B] [Result String]`

*Note: All integers are packed as **Big Endian** (`>I`).*

## 🧪 Testing
Run the example scripts against a local MaazDB server:
```bash
python examples/basic.py
```
```

### Summary of changes:
1.  **`README.md`**: Simplified for the end-user. It only shows how to install and run a basic query.
2.  **`DEVELOPER.md`**: Added the project tree, instructions for `pip install -e .` (editable mode), and the full build/publish workflow using `build` and `twine`.