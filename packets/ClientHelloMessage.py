import struct
from utils.writer import Writer

class ClientHelloMessage():
    def __init__(self):
        self.w = Writer()

    def add_header(self, data, id: int):
        header = b''
        header += self.w.writeShort(id)
        header += len(data).to_bytes(3, 'big')
        header += self.w.writeShort(0)
        header += data
        return header

    def send_client_hello(self, major: int, minor: int):
        message = b''
        message += self.w.writeInt(2)
        message += self.w.writeInt(11)
        message += self.w.writeInt(major)
        message += self.w.writeInt(0)
        message += self.w.writeInt(minor)
        message += self.w.writeInt(0)
        message += self.w.writeInt(2)
        message += self.w.writeInt(2)
        return self.add_header(message, 10100)
