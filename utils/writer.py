import struct

class Writer:
    def __init__(self, endian: str = 'big'):
        self.endian = endian
        self.buffer = b''

    def writeInt(self, integer: int, length: int = 1):
        return struct.pack('>I', integer)

    def writeShort(self, integer: int):
        return struct.pack('>H', integer)

