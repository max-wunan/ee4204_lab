import socket

HOST = ''  # Bind to all available network interfaces
PORT = 8000  # Port number to listen on

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the IP address and port number
s.bind((HOST, PORT))

# Receive data from clients and print it out
while True:
    data, address = s.recvfrom(1024)
    print(f"Received {len(data)} bytes from {address}: {data}")
