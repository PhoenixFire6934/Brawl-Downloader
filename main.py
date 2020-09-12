import socket
import struct
from requests import get
import json
from json import loads
import os


s = socket.socket()


def connect(url:str, port:int):
    try:
        s.connect((url, port))
        print(f"connecting to {url}:{port} ...")
    except:
        print("couldnt connect :(")
        return


def recvall(sock: socket.socket, packet_length: int):
    received_data = b''
    while packet_length > 0:
        s = sock.recv(packet_length)
        if not s:
            raise EOFError
        received_data += s
        packet_length -= len(s)
    return received_data


def add_header(data, id:int):
    header = b''
    header+= struct.pack('>H', id)
    header+= len(data).to_bytes(3, 'big')
    header += struct.pack('>H', 0)
    header+= data
    return header


def send_packet(major:int, minor:int):
    message = b''
    message += struct.pack('>I', 2)
    message += struct.pack('>I', 11)
    message += struct.pack('>I', major)
    message += struct.pack('>I', 0)
    message += struct.pack('>I', minor)
    message += struct.pack('>I', 0)
    message += struct.pack('>I', 2)
    message += struct.pack('>I', 2)
    s.send(add_header(message, 10100))


def read_string(data, lenn):
    string = ''
    y = -1
    for x in range(0, lenn):
        string += data[y:x].decode('utf-8', errors = 'ignore')
        y += 1
    return string

def read_int(data):
    int = struct.unpack('>I', data[:4])[0]
    return int

def read_short(data):
    short = struct.unpack('>H', data[:2])[0]
    return short

def get_response():
    i = 0
    int_len = 4
    short_len = 2
    byte_len = 1

    header = s.recv(7)
    packet_length = int_len.from_bytes(header[2:5], 'big')
    data = recvall(s, packet_length)
    print(data)

    error_code = read_int(data)
    i += int_len
    if error_code == 7:
        finger_len = read_int(data[i:])
        i += int_len
        finger = read_string(data[i:], finger_len +1 )
        finger = loads(finger)
        i += finger_len
        read_int(data[i:])
        i += int_len
        first_url_len = read_int(data[i:])
        i += int_len
        read_string (data[i:], first_url_len +1 )
        i += first_url_len
        read_int(data[i:])
        i += int_len
        read_int(data[i:])
        i += int_len
        read_int(data[i:])
        i += int_len
        read_int(data[i:])
        i += int_len
        read_int(data)
        i += int_len
        read_short(data[i:])
        i += short_len
        i += byte_len
        second_url_len = read_short(data[i:])
        i += short_len
        read_string(data[i:], second_url_len +1 )
        i += second_url_len
        read_short(data[i:])
        i += short_len
        third_url_len = read_short(data[i:])
        i += short_len
        assets_url = read_string(data[i:], third_url_len+1)

        x = json.dumps(finger)
        fingerprint = json.loads(x)

        for i in fingerprint['files']:
            path, name = os.path.split(i['file'])
            request = get(f'{assets_url}/{finger["sha"]}/{path}/{name}')
            status_code = request.status_code
            if status_code == 200:
                print(f"downloading {path}/{name} ...")
                filedata = request.content

                if not os.path.isdir(path):
                    os.mkdir(f'{path}')

                with open(os.path.join(f'{path}/{name}'), 'wb') as out:
                    out.write(filedata)
                    out.close()
    else:
        print(f"recived {error_code} error code ... returning")
        return


connect('game.brawlstarsgame.com', 9339)
send_packet(29, 500)
get_response()



