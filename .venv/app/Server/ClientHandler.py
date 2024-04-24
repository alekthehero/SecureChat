import threading
import socket

class ClientHandler:

    def __init__(self, client_socket: socket.socket, client_address: socket.AddressInfo):
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
                print(f"Received: {data.decode()}")
                self.client_socket.sendall("Connection Established".encode())
                # Compare this data from the databse.txt file
                # username:password
                with open(".venv\\app\\Utility\\database.txt", "r") as file:
                    found = False
                    for line in file:
                        entry = line.strip()
                        print(f"Entry: {entry}")
                        if data.decode() == entry:
                            self.client_socket.sendall("Login Successful".encode())
                            found = True
                            break
                    else:
                        self.client_socket.sendall("Login Failed".encode())

                    if found: break

                    self.client_socket.sendall("Creating Account".encode())
                    # Append the new line to the database.txt file
                    with open(".venv\\app\\Utility\\database.txt", "a") as file:
                        file.write(data.decode() + "\n")

                    break