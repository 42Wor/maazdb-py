import socket
import ssl
import struct
from . import protocol
from .exceptions import ConnectionError, AuthError, ProtocolError

class MaazDB:
    def __init__(self):
        self.sock = None
        self.connected = False

    def connect(self, host, port, user, password):
        """
        Establishes a Secure TLS 1.3 Connection to MaazDB.
        """
        try:
            # 1. Create Raw TCP Socket
            raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            raw_sock.settimeout(10) # 10s timeout

            # 2. Create SSL Context
            # NOTE: For self-signed certs (Dev Mode), we disable verification.
            # In production, you would load a CA file here.
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE 

            # 3. Wrap Socket (Upgrade to TLS)
            self.sock = context.wrap_socket(raw_sock, server_hostname=host)
            self.sock.connect((host, port))

            # 4. Perform Handshake
            # Payload: user\0password\0signature
            payload = f"{user}\0{password}\0{protocol.DRIVER_SIG}"
            packet = protocol.pack_packet(protocol.PACKET_HANDSHAKE, payload)
            self.sock.sendall(packet)

            # 5. Read Auth Response
            ptype, response = self._read_packet()
            
            if ptype == protocol.PACKET_AUTH_OK:
                self.connected = True
                return self
            elif ptype == protocol.PACKET_AUTH_ERR:
                raise AuthError(f"Authentication Failed: {response}")
            else:
                raise ProtocolError(f"Unexpected handshake response: {ptype}")

        except socket.error as e:
            raise ConnectionError(f"Could not connect to {host}:{port} - {e}")

    def query(self, sql):
        """
        Sends a SQL query and returns the result string.
        """
        if not self.connected:
            raise ConnectionError("Not connected to server")

        try:
            # Send Query
            packet = protocol.pack_packet(protocol.PACKET_QUERY, sql)
            self.sock.sendall(packet)

            # Read Result
            ptype, response = self._read_packet()

            if ptype in (protocol.PACKET_MSG, protocol.PACKET_DATA):
                return response
            elif ptype == protocol.PACKET_AUTH_ERR:
                self.close()
                raise AuthError("Session expired")
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
        """Internal helper to read exactly one packet."""
        # 1. Read Header (5 bytes)
        header_data = self._recv_exact(5)
        if not header_data:
            raise ConnectionError("Server closed connection")
        
        ptype, length = protocol.unpack_header(header_data)

        # 2. Read Payload
        payload_data = self._recv_exact(length)
        return ptype, payload_data.decode('utf-8', errors='replace')

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