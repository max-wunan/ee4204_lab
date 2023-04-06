import socket

HOST = '127.0.0.1'  # IP address of the server
PORT = 8000  # Port number of the server

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send a message to the server
message = b'Hello, world!'
s.sendto(message, (HOST, PORT))

# Close the socket
s.close()
