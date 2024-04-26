import threading
import socket
import os


class ClientHandler:

    def __init__(self, client_socket: socket.socket, client_address: socket.AddressInfo, logger: callable):
        self.data = None
        self.client_thread = None
        self.logger = logger

        self.client_socket = client_socket
        self.client_address = client_address

    def Start(self):
        #Start a thread to handle itself
        self.client_thread = threading.Thread(target=self.HandleClient)
        self.client_thread.start()

    def HandleClient(self):
        with self.client_socket:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                self.data = data.decode()

                split_data = self.data.split(":")
                if split_data[0] == "login":
                    if self.handle_login(split_data[1], split_data[2]):
                        break
                elif split_data[0] == "create":
                    if self.handle_create(split_data[1], split_data[2]):
                        break

    def handle_login(self, username, hashed_password):
        with open(os.getcwd() + "/src/Utility/database.txt", "r") as file:
            for line in file:
                entry = line.strip()
                split_entry = entry.split(":")
                if username == split_entry[0] and hashed_password == split_entry[1]:
                    message = "success:" + split_entry[2]  # entry 2 will be the guid
                    self.client_socket.sendall(message.encode())
                    self.logger(f"User {username}   GUID: {split_entry[2]}   has logged in successfully")
                    return True

            message = "fail:Invalid username or password"
            self.client_socket.sendall(message.encode())
            self.logger(f"User, {username}, failed to log in from: {self.client_address}")
            return False

    def handle_create(self, username, hashed_password):

        with open(os.getcwd() + "/src/Utility/database.txt", "a") as file:
            # Check if the username already exists
            with open(os.getcwd() + "/src/Utility/database.txt", "r") as read_file:
                for line in read_file:
                    entry = line.strip()
                    split_entry = entry.split(":")
                    if username == split_entry[0]:
                        message = "fail:User already exists"
                        self.client_socket.sendall(message.encode())
                        self.logger(f"User, {username}, exists already when trying to create account")
                        return False

            # generate a guid for the user based on their username
            guid = str(hash(username))
            file.write(username + ":" + hashed_password + ":" + guid + "\n")
            message = "success:" + guid
            self.client_socket.sendall(message.encode())
            self.logger(f"User {username}   GUID: {guid}   has been created successfully")
            return True
