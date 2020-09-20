import socket
from packets.ClientHelloMessage import ClientHelloMessage
from downloader import Downloader
from utils.reader import Reader
from requests import get
import json
import sys
import os


def _(*args):
    print('[Tool] ', end='')
    for arg in args:
        print(arg, end=' ')
    print()


class Connection():
    def __init__(self):
        self.s = socket.socket()
        self.client_hello = ClientHelloMessage()

    def connect(self, url:str, port:int):
        try:
            self.s.connect((url, port))
            _(f"Connecting to {url}:{port} ...\n")
        except:
            _("Failed to connect")
            return

    def recvall(self, sock: socket.socket, packet_length: int):
        received_data = b''
        while packet_length > 0:
            s = sock.recv(packet_length)
            if not s:
                raise EOFError
            received_data += s
            packet_length -= len(s)
        return received_data


    def send_packet(self, major:int, minor:int):
        packet = self.client_hello.send_client_hello(major, minor)
        self.s.send(packet)


    def get_response(self):
        int_len = 4
        header = self.s.recv(7)
        packet_length = int_len.from_bytes(header[2:5], 'big')
        data = self.recvall(self.s, packet_length)
        r = Reader(data)
        code = r.readUInt32()

        if code == 7 or code == 8:
            self.fingerprint = json.loads(r.readFinger()) # fingerprint
            r.readInt32()
            r.readShort()
            self.assets_url = r.readString() # assets url
            r.skip(23)
            r.readString()
            r.skip(2)
            r.readString()

            d = Downloader(self.fingerprint, self.assets_url)
            d.download()
        else:
            _(f"Recived code {code} - returning!")
            return



if __name__ == '__main__':
    try:
        config = open('config.json', 'r')
        content = config.read()
    except FileNotFoundError:
        _("Failed to load config.json!")
        sys.exit()

    settings = json.loads(content)

    host = settings['hostname']
    port = settings['port']
    major = settings['major_version']
    minor = settings['minor_version']

    downloader = Connection()
    downloader.connect(host, port)
    downloader.send_packet(major, minor)
    downloader.get_response()



