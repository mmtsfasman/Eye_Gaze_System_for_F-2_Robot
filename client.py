import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 6069
string = sys.argv[1]
s.connect((host, port))
bytes = string.encode('utf-8')
s.send(len(bytes).to_bytes(4,byteorder='little')+string.encode('utf-8'))
s.close()