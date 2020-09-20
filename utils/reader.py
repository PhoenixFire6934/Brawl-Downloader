import io

class Reader:
    def __init__(self, data):
        self.stream = io.BytesIO(data)

    def readByte(self):
        return int.from_bytes(self.stream.read(1), 'big')

    def readUInt16(self):
        return int.from_bytes(self.stream.read(2), 'big')

    def readInt16(self):
        return int.from_bytes(self.stream.read(2), 'big', signed = True)

    def readUInt32(self):
        return int.from_bytes(self.stream.read(4), 'big')

    def readInt32(self):
        return int.from_bytes(self.stream.read(4), 'big', signed = True)

    def readChar(self, length: int = 1) -> str:
        return self.stream.read(length).decode('utf-8')

    def readString(self) -> str:
        length = self.readUInt16()
        return self.readChar(length)

    def skip(self, num):
        for i in range(0, num):
            self.readByte()

    def readFinger(self) -> str:
        length = self.readInt32()
        return self.readChar(length)

    readShort = readUInt16
