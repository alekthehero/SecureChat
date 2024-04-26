import threading
import socket
import ssl
from src.Server.ClientHandler import ClientHandler


class TCPServer:
    def __init__(self, host, port, logger: callable):
        self.host = host
        self.port = port
        self.logger = logger
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Wrap the socket with SSL
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile="certs/cert.pem", keyfile="certs/key.pem")
        self.server = context.wrap_socket(self.server, server_side=True)

        self.server.bind((self.host, self.port))
        self.server.listen(5)
        self.active = True

        # Thread the sever so that it doesn't pause the GUI thread
        self.server_thread = threading.Thread(target=self.listen)
        self.server_thread.daemon = True
        self.server_thread.name = "ServerThread"
        self.server_thread.start()

    def listen(self):
        self.logger(f"Server is listening on {self.host}:{self.port}")
        while self.active:
            try:
                client, address = self.server.accept()
                if self.active:  # Check if we are still active after getting a client
                    self.logger(f"Connection from {address}")
                    client_handler = ClientHandler(client, address, self.logger)
                    client_handler.Start()
                else:
                    client.close()
            except Exception as e:
                if self.active:  # Only log errors if we didn't expect the socket to be closed
                    self.logger(f"Error accepting connections: {e}")
                break

    def close(self):
        self.active = False
        self.server.close()
        self.logger("Server closed")
