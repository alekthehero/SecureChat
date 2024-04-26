import socket
import threading
import ssl
import hashlib
import os


class Client:

    def __init__(self, logger: callable):
        self.logger = logger

        self.server_address = ('localhost', 12345)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print(os.getcwd())
        ssl_context = ssl.create_default_context()
        ssl_context.load_verify_locations(os.getcwd() + "/certs/cert.pem")

        ssl_context.check_hostname = False

        self.client_socket = ssl_context.wrap_socket(self.client_socket, server_hostname="localhost")

        self.client_thread = threading.Thread(target=self.connect)
        self.client_thread.daemon = True
        self.client_thread.start()

    def connect(self):
        self.client_socket.connect(self.server_address)

        while True:
            data = self.client_socket.recv(1024)
            # first part of message before colon is success or fail, after success will come guid
            split_data = data.decode().split(":")
            if split_data[0] == "success":
                self.logger(split_data[1])
                break
            elif split_data[0] == "fail":
                self.logger(split_data[1])
                break

    def close(self):
        self.client_socket.close()

    def send_login(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        message = f"login:{username}:{hashed_password}"
        self.client_socket.sendall(message.encode())

    def send_create(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        message = f"create:{username}:{hashed_password}"
        self.client_socket.sendall(message.encode())
