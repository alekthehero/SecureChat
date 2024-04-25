import threading
import socket
import ssl
from src.Server.ClientHandler import ClientHandler

class TCPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Wrap the socket with SSL
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile="certs/cert.pem", keyfile="certs/key.pem")
        self.server = context.wrap_socket(self.server, server_side=True)

        self.server.bind((self.host, self.port))
        self.server.listen(5)

    def listen(self):
        print(f"Server is listening on {self.host}:{self.port}")
        while True:
            client, address = self.server.accept()
            print(f"Connection from {address}")
            client_handler = ClientHandler(client, address)
            client_handler.Start()

if __name__ == "__main__":
    server = TCPServer('localhost', 12345)
    server.listen()