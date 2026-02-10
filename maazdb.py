import socket
import struct

# Protocol Constants
PACKET_HANDSHAKE = 0x10
PACKET_AUTH_OK   = 0x11
PACKET_AUTH_ERR  = 0x12
PACKET_QUERY     = 0x20
PACKET_MSG       = 0x02
PACKET_DATA      = 0x03

# Official Driver Signature
DRIVER_SIGNATURE = "maazdb-python-driver-v1"

class MaazDBError(Exception):
    pass

class MaazDBAuthError(MaazDBError):
    pass

class MaazDB:
    def __init__(self):
        self.sock = None
        self.connected = False

    def connect(self, host, port, username, password):
        """
        Establishes a persistent connection and performs the secure handshake
        with the official driver signature.
        """
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))
            
            # 1. Construct Handshake Payload: "username\0password\0signature"
            # This proves to the server that we are using the official driver.
            credentials = f"{username}\0{password}\0{DRIVER_SIGNATURE}".encode('utf-8')
            
            # 2. Send Handshake Packet
            self._send_packet(PACKET_HANDSHAKE, credentials)
            
            # 3. Wait for Auth Response
            ptype, payload = self._read_packet()
            
            if ptype == PACKET_AUTH_OK:
                self.connected = True
                return True
            elif ptype == PACKET_AUTH_ERR:
                error_msg = payload.decode('utf-8')
                self.sock.close()
                raise MaazDBAuthError(f"Authentication Failed: {error_msg}")
            else:
                self.sock.close()
                raise MaazDBError(f"Unexpected packet during handshake: {ptype}")
                
        except Exception as e:
            if self.sock:
                self.sock.close()
            raise e

    def query(self, sql):
        """
        Sends a SQL query over the existing connection and returns the result.
        Does NOT reconnect; keeps the session alive.
        """
        if not self.connected:
            raise MaazDBError("Not connected to database")

        self._send_packet(PACKET_QUERY, sql.encode('utf-8'))
        
        ptype, payload = self._read_packet()
        response = payload.decode('utf-8').strip()
        
        if ptype == PACKET_MSG:
            return {"status": "message", "content": response}
        elif ptype == PACKET_DATA:
            # Basic CSV parsing for now, based on server output
            rows = []
            if response:
                for line in response.split('\n'):
                    if line.strip():
                        rows.append(line.split(', '))
            return {"status": "data", "rows": rows}
        else:
            return {"status": "unknown", "content": response}

    def close(self):
        """
        Closes the connection gracefully.
        """
        if self.sock:
            self.sock.close()
        self.connected = False

    def _send_packet(self, ptype, payload):
        # Header: [Type (1 byte)] [Length (4 bytes Big Endian)]
        length = len(payload)
        header = struct.pack('>BI', ptype, length)
        self.sock.sendall(header + payload)

    def _read_packet(self):
        # Read Header (5 bytes)
        header = self._recv_exact(5)
        if not header:
            raise MaazDBError("Connection closed by server")
            
        ptype, length = struct.unpack('>BI', header)
        
        # Read Payload
        payload = self._recv_exact(length)
        return ptype, payload

    def _recv_exact(self, n):
        data = b''
        while len(data) < n:
            packet = self.sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

# --- Usage Example ---
if __name__ == "__main__":
    db = MaazDB()
    
    try:
        print("Connecting...")
        # Default admin credentials created by system catalog
        db.connect("127.0.0.1", 8888, "admin", "admin") 
        print("Connected successfully!")
        
        print("\nCreating Database...")
        print(db.query("CREATE DATABASE mydb"))
        
        print("\nUsing Database...")
        print(db.query("USE mydb"))
        
        print("\nCreating Table...")
        print(db.query("CREATE TABLE users (id INT PRIMARY KEY, name TEXT)"))
        
        print("\nInserting Data...")
        print(db.query("INSERT INTO users VALUES (1, 'Maaz')"))
        print(db.query("INSERT INTO users VALUES (2, 'Alice')"))
        
        print("\nSelecting Data...")
        result = db.query("SELECT * FROM users")
        for row in result['rows']:
            print(row)
            
    except MaazDBAuthError as e:
        print(f"Login Failed: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()