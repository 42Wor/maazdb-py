# FILE PATH: maazdb-py/maazdb/protocol.py

import struct

# Constants matching MaazDB v13.5+ Server
PACKET_CHALLENGE_REQ  = 0x10
PACKET_CHALLENGE_RESP = 0x11
PACKET_AUTH_OK        = 0x12
PACKET_AUTH_ERR       = 0x13
PACKET_QUERY          = 0x20
PACKET_MSG            = 0x02
PACKET_DATA           = 0x03

# Protocol Flags
FLAG_NONE       = 0x00
FLAG_EARLY_DATA = 0x02 # 0-RTT Safe Flight

DRIVER_SIG = "maazdb-python-sdk-v1"

def pack_packet(ptype, flags, req_id, payload):
    """
    Creates a binary packet: [Type (1B)] [Flags (1B)] [Req ID (2B)] [Length (4B)] [Payload]
    All integers are packed using Big-Endian formatting.
    """
    if isinstance(payload, str):
        payload = payload.encode('utf-8')
    
    length = len(payload)
    # >B   = Unsigned Char (1 byte)
    # >H   = Unsigned Short (2 bytes)
    # >I   = Unsigned Int (4 bytes)
    header = struct.pack('>BBHI', ptype, flags, req_id, length)
    return header + payload

def unpack_header(data):
    """
    Unpacks the 8-byte header. Returns (ptype, flags, req_id, length).
    """
    if len(data) < 8:
        return None
    return struct.unpack('>BBHI', data)