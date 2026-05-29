# FILE PATH: maazdb-py/maazdb/client.py

import socket
import ssl
import hmac
import hashlib
from . import protocol
from .exceptions import ConnectionError, AuthError, ProtocolError

class MaazDB:
    def __init__(self):
        self.sock = None
        self.connected = False
        self.next_req_id = 0

    def connect(self, host, port, user, password):
        """
        Establishes a Secure TLS 1.3 Connection to MaazDB and authenticates.
        """
        try:
            # 1. Create Raw TCP Socket
            raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            raw_sock.settimeout(10) # 10s timeout
            raw_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

            # 2. Create SSL Context (Upgrade to TLS)
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE 

            self.sock = context.wrap_socket(raw_sock, server_hostname=host)
            self.sock.connect((host, port))

            # 3. Read CHALLENGE_REQ from Server
            ptype, flags, req_id, challenge_data = self._read_packet()
            
            if ptype != protocol.PACKET_CHALLENGE_REQ:
                raise ProtocolError(f"Unexpected initial handshake packet: {hex(ptype)}")

            # 4. Compute HMAC-SHA256 Signature (Payload is the 32-byte nonce)
            mac = hmac.new(password.encode('utf-8'), challenge_data, hashlib.sha256)
            signature_hex = mac.hexdigest()

            # 5. Send CHALLENGE_RESP (Payload: Username \0 Password \0 DriverID \0 SignatureHex)
            payload = f"{user}\0{password}\0{protocol.DRIVER_SIG}\0{signature_hex}"
            packet = protocol.pack_packet(protocol.PACKET_CHALLENGE_RESP, protocol.FLAG_NONE, 0, payload)
            self.sock.sendall(packet)

            # 6. Read Auth Result
            ptype, flags, req_id, auth_result_data = self._read_packet()
            auth_msg = auth_result_data.decode('utf-8', errors='replace')
            
            if ptype == protocol.PACKET_AUTH_OK:
                self.connected = True
                return self
            elif ptype == protocol.PACKET_AUTH_ERR:
                raise AuthError(f"Authentication Failed: {auth_msg}")
            else:
                raise ProtocolError(f"Unexpected auth verification response: {ptype}")

        except socket.error as e:
            raise ConnectionError(f"Could not connect to {host}:{port} - {e}")

    def query(self, sql):
        """
        Sends a SQL query and returns the result string.
        """
        if not self.connected:
            raise ConnectionError("Not connected to server")

        try:
            # Feature: Automated 0-RTT safe flight flag mapping
            flags = protocol.FLAG_NONE
            upper_sql = sql.strip().upper()
            if upper_sql.startswith("SELECT") or upper_sql.startswith("SHOW") or upper_sql.startswith("DESCRIBE") or upper_sql.startswith("DESC"):
                flags |= protocol.FLAG_EARLY_DATA

            # Increment Request ID (wraps at 65535)
            self.next_req_id = (self.next_req_id + 1) % 65536

            # Send Query
            packet = protocol.pack_packet(protocol.PACKET_QUERY, flags, self.next_req_id, sql)
            self.sock.sendall(packet)

            # Read Result
            ptype, flags, req_id, response_data = self._read_packet()
            response_str = response_data.decode('utf-8', errors='replace')

            if ptype in (protocol.PACKET_MSG, protocol.PACKET_DATA):
                return response_str
            elif ptype == protocol.PACKET_AUTH_ERR:
                self.close()
                raise AuthError(f"Session expired or rejected: {response_str}")
            else:
                raise ProtocolError(f"Unknown packet type: {ptype}")

        except socket.error as e:
            self.close()
            raise ConnectionError(f"Network error during query: {e}")

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            except:
                pass
        self.connected = False

    def _read_packet(self):
        """Internal helper to read exactly one v2.1 packet."""
        # Read 8-byte header
        header_data = self._recv_exact(8)
        if not header_data:
            raise ConnectionError("Server closed connection")
        
        ptype, flags, req_id, length = protocol.unpack_header(header_data)

        # Read variable-length payload
        payload_data = self._recv_exact(length) if length > 0 else b''
        return ptype, flags, req_id, payload_data

    def _recv_exact(self, n):
        """Reads exactly n bytes from the socket."""
        data = b''
        while len(data) < n:
            packet = self.sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    # Context Manager Support (with MaazDB() as db:)
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()