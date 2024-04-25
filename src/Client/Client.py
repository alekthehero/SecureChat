import socket
import ssl
import hashlib
import os

# Define the server address and port
server_address = ('localhost', 12345)

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Create SSL context
print(os.getcwd())
ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(os.getcwd() + "/certs/cert.pem")

ssl_context.check_hostname = False

# Wrap the socket with SSL
client_socket = ssl_context.wrap_socket(client_socket, server_hostname="localhost")

# Get user input for usernmae and password and hash it 
username = input("Enter username: ")
password = input("Enter password: ")
hashed_password = hashlib.sha256(password.encode()).hexdigest()
print(f"Hashed password: {hashed_password}")

# Connect to the server
client_socket.connect(server_address)

# Send data to the server
message = f"{username}:{hashed_password}"
client_socket.sendall(message.encode())

# Receive data from the server
while True:
    data = client_socket.recv(1024)
    print("Received:", data.decode())
    if data.decode() == "Login Successful":
        break
    elif data.decode() == "Creating Account":
        break

# Close the connection
client_socket.close()
