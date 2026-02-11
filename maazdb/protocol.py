import struct

# Constants matching Rust Server
PACKET_HANDSHAKE = 0x10
PACKET_AUTH_OK   = 0x11
PACKET_AUTH_ERR  = 0x12
PACKET_QUERY     = 0x20
PACKET_MSG       = 0x02
PACKET_DATA      = 0x03

# Driver Signature (Must match ALLOWED_DRIVERS in Rust Server)
DRIVER_SIG = "maazdb-python-sdk-v2"

def pack_packet(ptype, payload):
    """
    Creates a binary packet: [Type (1B)] [Length (4B Big Endian)] [Payload]
    """
    if isinstance(payload, str):
        payload = payload.encode('utf-8')
    
    length = len(payload)
    # >B = Big Endian Unsigned Char (1 byte)
    # >I = Big Endian Unsigned Int (4 bytes)
    header = struct.pack('>BI', ptype, length)
    return header + payload

def unpack_header(data):
    """
    Unpacks the 5-byte header. Returns (ptype, length).
    """
    if len(data) < 5:
        return None
    return struct.unpack('>BI', data)