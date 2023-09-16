import socket
from threading import Thread

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 5431
serversocket.bind((host, port))


class Client(Thread):
    def __init__(self, _socket, _address):
        Thread.__init__(self)
        self.sock = _socket
        self.addr = _address
        self.credentials = None
        self.start()

    def run(self):
        while True:
            try:
                recv = self.sock.recv(1024).decode()
            except ConnectionResetError:
                break



serversocket.listen(5)
print("Server started and listening")
try:
    while True:
		print("loop")
        clientsocket, address = serversocket.accept()
        clients.append(Client(clientsocket, address))
        print("a")
finally:
    serversocket.close()
